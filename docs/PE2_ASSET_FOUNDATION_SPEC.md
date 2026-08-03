# PE-2 Asset Foundation Specification

Status: **PE-2.0 COMPLETE - DESIGN APPROVED; PE-2.1 NOT STARTED**

## Purpose and scope

PE-2.1 will introduce the first durable Asset-layer capability: operator-managed
friendly naming and physical-location metadata. This specification closes the
product and architecture decisions required for implementation. It does not
implement the store, CLI, runtime state, presentation, publication, expected
availability, lifecycle policy, or any production change.

The permanent layers remain:

- **Observation:** what HIOC or a source saw, with source and time semantics.
- **Enrichment:** what HIOC normalized, correlated, selected, or inferred.
- **Asset:** what the operator intentionally knows and manages about a real-world
  thing linked to HIOC stable identity.

No layer rewrites another. Asset metadata is the highest descriptive authority
for its own fields, but it is not identity, canonical-address, liveness, health,
incident, topology, or service-ownership authority.

PE-2.1 is storage and governed editing only. It adds no public projection, UI,
MQTT topic, Home Assistant entity, dashboard input, notification, incident field,
or inventory-engine dependency.

## Current operator-metadata audit

Current fields cannot silently become Asset fields:

| Current field or surface | Current ownership and meaning | Exposure and consumers | Asset reuse decision and risk |
| --- | --- | --- | --- |
| Device `id` | Derived by `stable_device_id()` from MAC, then IP, hostname, configured ID, or name | Public inventory, MQTT, HA, events, topology and services | Link key only. Asset never supplies or recalculates it. Weak IDs can later be superseded; no alias contract exists. |
| `mac` / `ip` | Observed/configured technical identity and canonical address evidence | Public inventory and operational consumers | Never Asset keys or editable Asset fields. IP changes must not move metadata. |
| `hostname` | Selected technical hostname from current source authority | Public inventory, MQTT, HA and dashboards | Observation/technical metadata only. Asset friendly name never replaces it. |
| `name` | Source metadata, then overwritten by current display fallback | Public inventory, MQTT, HA and dashboards | Overloaded and incompatible with durable Asset meaning. No reinterpretation. |
| `display_name` | Derived each merge as `name`, hostname, IP, then ID | Public inventory; dashboard sorting/display; events, incidents, topology and service labels | Presentation field with broad compatibility risk. PE-2.1 leaves it byte/semantically unchanged. |
| `role` | Known/integration value when approved, otherwise inferred `operator_role()` category | Public inventory, monitoring policy, dashboards and correlation | Operationally significant and overloaded. Deferred; Asset purpose cannot replace it. |
| `inventory_class` | Derived from `role` as infrastructure/client | Public inventory, health/monitoring and dashboards | Derived operational field; never Asset metadata. |
| `location` / `area` | Optional known-infrastructure or integration metadata, merged into public inventory | Public inventory and MQTT when present; potential dashboard consumer | Overloaded, weakly validated, and already public. Preserve unchanged; new `physical_location` remains private and separate. |
| `notes` | Optional known-infrastructure/integration metadata merged into public inventory | Public inventory and MQTT when present | Privacy and compatibility risk. Preserve existing behavior; new Asset `notes` is a separate private value. |
| `vendor`, `model`, `type` | Known, integration, observed, or derived descriptive metadata | Public inventory and consumers | Not PE-2.1 fields. Manufacturer/model work belongs to later packages. |
| Known-infrastructure file | Manually edited configuration accepted by a permissive field set; can provide identity, name, role, topology, location and notes | Feeds public inventory and operational logic | Remains supported input. It is not migrated automatically and is not the Asset write path. |
| Integration JSON | Source-provided device dictionaries with technical and descriptive metadata | Feeds public inventory | Not operator authority. Integration names may later be presentation suggestions but never overwrite Asset fields. |
| Service `name`, `host`, `device_id` | Discovered service identity and current inventory-derived owner label | Public services, MQTT, HA, dashboards, topology/dependencies | Service ownership is not human ownership and is unchanged. |
| Topology labels | Derived from current `display_name`, role, IDs, and relationship evidence | Public topology and dashboards | No Asset projection in PE-2.1. |
| HA entity names/friendly names | Repository-defined consumer presentation | Home Assistant and dashboards | Not read or changed; no Asset authority. |
| Dashboard labels | Static YAML labels or current public inventory fields | Operator UI | No change in PE-2.1. Future opt-in projection needs separate review. |

Compatibility path: known-infrastructure, integration, public `name`,
`display_name`, `location`, and `notes` continue unchanged. PE-2.1 creates a
parallel private store. A later presentation checkpoint may explicitly select
Asset `friendly_name` for a new projection while retaining technical hostname
and compatibility fallbacks; it must review every MQTT, HA, dashboard, incident,
topology, and service consumer before doing so.

Repository source map and classification:

| Subject | Authoritative current location | Current classification | Public/MQTT/dashboard | Identity or canonical bearing | PE-2.1 disposition |
| --- | --- | --- | --- | --- | --- |
| `name`, `hostname`, `display_name` | `pi4/lib/hioc/inventory.py`; public device dictionaries; `docs/DATA_MODEL.md` | `hostname` observed/configured; `name` overloaded source/fallback; `display_name` derived | All can be public/MQTT; HA inventory and dashboards consume current names | Hostname/name can be weak identity fallback today; none may receive Asset input | Preserve unchanged; new friendly name stays separate |
| `role`, `inventory_class` | `operator_role()`, `inventory_class()`, monitoring/correlation code and tests | Configured or derived operational classification | Public/MQTT/dashboard/correlation | Not canonical address, but affects monitoring/health semantics | Not reusable for Asset purpose |
| `location`, `area`, current `notes` | `KNOWN_FIELDS`, `KNOWN_METADATA_FIELDS`, integration dictionaries and public devices | Optional configured/integration metadata; overloaded and weakly validated | Can enter public inventory/MQTT and future dashboard templates | Not canonical, but merged into technical records | Preserve; never copy or reinterpret automatically |
| `owner`, `purpose`, `friendly_name`, `physical_location` | No current runtime/schema field; planning references only | Absent | Not published | No identity/canonical authority | New private fields are governed only by this specification; owner deferred |
| Known-infrastructure manual file | `config/inventory/known_infrastructure.json`; `_clean_known_record()` | Operator-edited configuration mixed with identity/topology/public metadata | Accepted values merge into public inventory | MAC/IP/hostname/configured ID can participate in matching/identity | Remains supported; not Asset storage or migration source |
| Configured integration files | `state/inventory/integrations/*.json`; `integration_inventory()` | Trusted only within current merge rules; observed/configured meaning can be ambiguous | Merged public inventory/MQTT | May provide identity candidates and parent hints | Read nowhere by Asset CLI except public stable-ID inventory context |
| Dashboard/HA labels | `homeassistant/packages/hioc_living_inventory.yaml`, `homeassistant/dashboards/*.yaml` | Static consumer names plus public device `display_name`/`hostname` | UI-visible | Not identity/canonical authority | No change or Asset input in PE-2.1 |
| Service owner/host fields | `build_services()`, `enrich_services()`, public service model | Derived technical relationship keyed by `device_id` | Public/MQTT/HA/dashboard | Relationship-bearing, not human owner | Human owner is not reused; service logic unchanged |
| Topology labels/edges | `build_topology()`, topology/dependency builders | Derived from current devices/services and parent evidence | Public/MQTT/dashboard/correlation | Stable IDs are relationship keys; labels use current public names | No Asset projection or relationship mutation |

There is no current Asset record, Asset schema, Asset status, Asset editor,
archive, or identity-alias table. Existing historical inventory retention copies
public device records forward; it is not Asset persistence and will not become
the Asset write path.

## Asset identity contract

An Asset record is durable operator metadata keyed by one current-format HIOC
stable device ID. Version 1.0 keys and each embedded `stable_device_id` must be
identical and match `^dev_[0-9a-f]{16}$`.

The key is never an IP, hostname, MAC alone, array position, source order, HA
identifier, entity ID, or MQTT topic. MAC may be displayed as read-only context
but is not stored in the Asset record.

Behavior is closed as follows:

- IP, hostname, or canonical-IP change with the same stable ID: the Asset remains
  attached without mutation.
- Stable MAC-backed ID with address changes: unchanged Asset attachment.
- Multiple MAC identities: separate Assets unless a future governed physical-
  asset association explicitly links them; PE-2.1 never infers this.
- Current identity merge/split or ID supersession: no automatic Asset merge,
  split, copy, or deletion. The old record becomes orphaned. A future identity-
  migration contract must define aliases and an explicit operator-confirmed
  migration transaction.
- Device absent from inventory: Asset remains valid, editable, and orphaned.
- Asset before current observation: allowed only through the CLI's explicit
  `--allow-orphan` option and a syntactically valid stable ID.
- Invalid or unknown-format ID: rejected. No repair or fallback key is created.

Asset identity never flows backward into inventory reconciliation. The CLI may
read `inventory.json` only to report current/orphan status; it does not mutate
inventory or add in-memory Asset references.

## Approved version 1.0 fields

All record keys are required and the object is closed. At least one of the four
operator fields must be non-null; clearing the last field removes the record as
an explicit, backed-up transaction.

| Field | Type and limits | Authority/editability | Privacy and exposure | Default/merge/conflict |
| --- | --- | --- | --- | --- |
| `stable_device_id` | Required string matching the key | System-copied from CLI argument; immutable | Technical, private | No merge; mismatch rejected |
| `friendly_name` | Nullable string, maximum 128 Unicode code points | Operator CLI | Sensitive; local only; future dashboard eligibility requires approval | `null`; operator value wins presentation only in a future projection; duplicates allowed |
| `physical_location` | Nullable string, maximum 128 code points | Operator CLI | Highly sensitive; local only | `null`; never inferred from network/HA area; no automatic merge |
| `purpose` | Nullable string, maximum 256 code points | Operator CLI | Sensitive; local only | `null`; distinct from role/class/domain/health/availability |
| `notes` | Nullable plain-text string, maximum 1,024 code points and 8 lines | Operator CLI | Highly sensitive; never routine output | `null`; no merge or rich-text interpretation |
| `created_at` | Required RFC 3339 UTC timestamp | System generated on first creation; immutable | Operational metadata; aggregate evidence only | Preserved on update |
| `updated_at` | Required RFC 3339 UTC timestamp | System generated on content-changing transaction | Operational metadata; aggregate evidence only | Unchanged by no-op |
| `update_source` | Required literal `operator_cli` | System generated | Non-sensitive | No alternate values in 1.0 |
| `revision` | Required integer >= 1 | System incremented on content change | Non-sensitive | Increment by one; optimistic compare supported |

`owner` is deferred. Current service ownership is technical, while human owner
could mean household member, administrator, responsible person, team, or legal
owner. The ambiguity and privacy risk are not justified by PE-2.1. It requires
a later terminology, access, and publication decision.

## Text normalization

All text is decoded as Unicode and normalized to NFC. NUL and Unicode control
characters are rejected. Maximums count normalized Unicode code points.

For `friendly_name`, `physical_location`, and `purpose`:

- trim leading and trailing Unicode whitespace;
- reject tabs, CR/LF, other line separators, and control characters;
- preserve internal printable characters and spacing;
- treat empty-after-trim input as an explicit clear to JSON `null`;
- do not case-fold, slugify, derive IDs, or require global uniqueness.

Duplicate friendly names are allowed because rooms and repeated equipment can
legitimately share labels. Matching and future display sorting must use stable ID
as the deterministic tie-break, never name as identity.

For `notes`:

- normalize CRLF/CR to LF, trim outer whitespace, and preserve internal text;
- allow at most eight lines; reject tabs and controls other than LF;
- empty-after-trim means clear to `null`;
- treat content as plain text, not Markdown, HTML, templates, or commands.

`physical_location` is one free-text field in 1.0. It describes physical
placement such as room, floor, rack, cabinet, wall, ceiling, garden, gate, or
driveway; it is never network location or HA area. This is the smallest useful,
privacy-bounded model. A later structured site/building/floor/room/area/mounting
model requires schema migration and explicit mapping; implementations must not
parse hierarchy from the free text.

`purpose` is free text describing operator intent. It is not a controlled
vocabulary and cannot set inventory role, class, HA domain, topology role,
health, criticality, or expected availability. A future category may be added
only by schema versioning.

## Asset storage schema

The authoritative local store is:

`state/inventory/assets.json`

Version 1.0 is deterministic, closed, and shaped exactly as:

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-01-01T00:00:00Z",
  "asset_count": 1,
  "assets": {
    "dev_0123456789abcdef": {
      "stable_device_id": "dev_0123456789abcdef",
      "friendly_name": "Synthetic Lab Device",
      "physical_location": null,
      "purpose": "Validation fixture",
      "notes": null,
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-01T00:00:00Z",
      "update_source": "operator_cli",
      "revision": 1
    }
  }
}
```

Top-level keys are required and no unknown keys are accepted. `updated_at` is
the last successful content-changing store transaction; initialization sets it.
`asset_count` equals mapping length. Mapping keys serialize in lexical order.
Record objects use the fixed keys above. JSON uses UTF-8, sorted keys, two-space
indentation, and a final newline. Empty store is valid with count zero and an
empty mapping. Unknown schema versions or fields fail closed; migration requires
an explicit versioned migrator, backup, validation, and rollback plan. There is
no extension object in 1.0.

The store is durable operator knowledge even though it lives beside inventory
state. It is excluded from Git and all release copy/overwrite behavior that
already preserves `state/`. Production values never enter fixtures or evidence.

## Asset status model

PE-2.1 also creates `state/inventory/assets_status.json`. The status is closed
version `1.0` with exactly:

- `schema_version`: `"1.0"`;
- `updated`: RFC 3339 UTC time of the latest validation attempt;
- `status`: `online`, `degraded`, `error`, or `unavailable`, matching existing
  subsystem conventions;
- `asset_count`: valid current record count;
- `orphaned_asset_count`: integer >= 0 when current inventory is valid, otherwise
  JSON `null`; valid Assets whose ID is absent from current inventory;
- `invalid_record_count`: zero for an online valid store, otherwise a sanitized
  count when determinable;
- `generator`: literal `hioc-assets`;
- `error_code`: null when online, otherwise a bounded lowercase code.

No error message, Asset value, ID, path, or exception text is stored. `online`
means store and inventory context validated. `degraded` means the Asset store is
valid but current inventory is missing/unavailable, so orphan count cannot be
authoritatively refreshed. `error` means malformed/unsupported Asset data or a
failed Asset transaction. `unavailable` means the store has not been initialized.
These states describe only the Asset subsystem and never device health.

## Governed editing path

Manual editing of `assets.json` is unsupported. PE-2.1 requires a small local
CLI because validation, timestamps, revision checks, backups, locks, modes, and
atomic writes must be one governed transaction. REST, HA services, dashboards,
and APIs are deferred.

Approved CLI surface:

- `hioc-assets.py initialize`
- `hioc-assets.py list` (all IDs, including orphan flag, but no field values)
- `hioc-assets.py show --device-id ID [--show-sensitive]`
- `hioc-assets.py set --device-id ID [--friendly-name VALUE]
  [--physical-location VALUE] [--purpose VALUE] [--notes VALUE]
  [--allow-orphan] [--expected-revision N]`
- `hioc-assets.py clear-field --device-id ID --field FIELD
  [--expected-revision N]`
- `hioc-assets.py remove --device-id ID [--expected-revision N]`
- `hioc-assets.py validate`
- `hioc-assets.py backup`
- `hioc-assets.py restore --backup PATH`

At least one field option is required for `set`. No-op normalized updates return
success without changing timestamps/revision or creating a backup. `list` and
default `show` redact sensitive values; `--show-sensitive` is explicit, local,
and never used in routine evidence. Import/export are deferred.

`initialize` creates a valid empty store and online/degraded status. Mutating CLI
commands validate and refresh status after the transaction. CLI `validate`
refreshes status without changing the Asset store. The standalone
`hioc-validate-assets.py` is read-only: it validates a supplied store/status pair
and emits sanitized PASS/FAIL output but never writes either artifact.

Synthetic production validation uses a syntactically valid reserved test ID,
`dev_0000000000000000`, with `--allow-orphan`, synthetic non-household values,
only after proving that ID is absent from current inventory and the Asset store,
then explicitly removes it after persistence/orphan/backup/restore checks. The
final production store must equal the pre-test semantic content. The temporary
test record must not remain.

## Atomic writes and concurrency

- Dedicated lock: `/tmp/hioc-assets.lock`; it is not the inventory lock.
- Every read-modify-write, backup, or restore holds an exclusive `flock` for the
  whole transaction. Read-only validate/list/show may use a shared lock.
- Acquisition timeout: five seconds. Timeout returns a sanitized nonzero result;
  no waiting is unbounded and no lock file is deleted as “stale.” Kernel lock
  ownership, not path existence, determines contention.
- Write a uniquely named temporary file in `state/inventory`, validate and
  `fsync` it, set `0600`, then `os.replace` the destination and `fsync` the
  directory. Clean temporary files on handled failure.
- State directory must be no broader than `0750`; Asset/status/temporary files
  are `0600`. Backup directory is `0700`; backup files are `0600`. Production
  ownership is `jazofv1:jazofv1`, matching the non-root runtime operator; the
  CLI refuses unexpected ownership rather than silently changing it.
- Re-read and validate under lock. `--expected-revision` rejects stale edits.
- Status write is separate and must not replace a valid store with partial data.

Asset locking never acquires the inventory lock and cannot block inventory
generation. Inventory is a read-only snapshot for orphan calculation.

## Failure isolation

Malformed or unsupported `assets.json` is never silently rewritten, discarded,
or partially loaded. Mutations are refused. The original bytes remain, status
is written as sanitized `error` where possible, and no Asset data is projected.
The subsystem does not automatically load a backup because silently reverting
operator knowledge can hide a newer change; recovery is an explicit validated
restore.

If inventory is missing or malformed while the Asset store is valid, Asset
editing with an existing record remains possible, creation requires explicit
`--allow-orphan`, and status is `degraded` with no fabricated orphan count.
Other HIOC functions continue.

Asset failure must not prevent inventory or enrichment generation, MQTT
publication, incidents, dashboards, HA, topology, or service ownership. The
Inventory Engine does not import or invoke the Asset subsystem in PE-2.1.

## Backup, restore, and recovery

Before every content-changing mutation or restore, create and validate a
timestamped backup at:

`backups/assets/assets-YYYYMMDDTHHMMSSffffffZ-<12-hex-content-digest>.json`

For first initialization, the backup is a valid empty version 1.0 store. Backup
creation and validation must succeed before replacement; otherwise mutation
fails. Backups are immutable through the CLI and are not automatically pruned in
PE-2.1. Retention policy is deferred rather than silently deleting durable
operator knowledge.

Restore accepts only a regular file beneath the configured Asset backup
directory, validates its closed schema, backs up the current bytes (including a
sanitized quarantine copy when malformed), atomically replaces the store, and
validates the result. Symlinks, traversal, arbitrary paths, and invalid versions
are rejected.

Release upgrade and rollback already preserve `state` and `backups`; PE-2.1 must
add regression proof. Asset metadata is included in future disaster-recovery
planning and replacement-host migration, but no off-device transport is
implemented. Operators are warned that local backups alone do not protect
against device loss; off-device encrypted backup policy remains future work.
Replacement-host recovery therefore requires an operator-controlled copy of the
store and Asset backup directory, followed by ownership/mode and schema
validation before any CLI mutation; PE-2.1 adds no transport automation.

PE-2.1 stores current state only. `created_at`, `updated_at`, `revision`, and
timestamped pre-mutation backups are its bounded audit evidence. `updated_by`,
human authentication, change reason, and an append-only audit log are deferred;
the CLI must not pretend that the operating-system account proves a human
identity.

## Lifecycle and orphan handling

Version 1.0 has no active, maintenance, retired, archived, or deleted lifecycle
field. Those meanings require later policy. Explicit record removal is a backed-
up metadata deletion, not a claim that the physical asset retired.

An orphan is a valid Asset whose stable ID is absent from the current valid
inventory snapshot. Orphans remain valid and editable, appear in CLI operational
views, and contribute to `orphaned_asset_count`. They are never automatically
deleted, merged, archived, marked unhealthy, or made into incidents. Temporary
observation loss, stale/offline state, maintenance, address change, or hostname
change does not change Asset content.

## Authority, coexistence, and conflicts

Asset values own only the matching Asset fields. Observation hostname and PE-1
Enrichment candidates remain intact. A different technical hostname and Asset
friendly name are not a data conflict because the fields answer different
questions. PE-2.1 stores no copied Observation/Enrichment candidates and no
dynamic conflict state.

A future presentation resolver may choose Asset `friendly_name`, then selected
Enrichment hostname, then existing public fallback, while labeling each layer.
That resolver and any disagreement display require separate approval. Concurrent
operator edits are true write conflicts and are rejected using revision checks;
identity supersession is surfaced as orphaning, not auto-resolution.

## Publication and privacy boundary

Version 1.0 is deny-by-default and local only. No Asset field or record may enter
public inventory JSON, MQTT, HA, dashboards, notifications, incidents, routine
logs, public APIs, events, topology, services, or support bundles.

Privacy classification:

| Field | Level | Future dashboard | Future notification | Future MQTT |
| --- | --- | --- | --- | --- |
| `friendly_name` | Sensitive household metadata | Eligible only after explicit projection/privacy review | Prohibited by default | Prohibited by default |
| `physical_location` | Highly sensitive | Restricted opt-in only | Prohibited by default | Prohibited by default |
| `purpose` | Sensitive operational/household metadata | Restricted opt-in only | Prohibited by default | Prohibited by default |
| `notes` | Highly sensitive free text | Prohibited by default | Prohibited | Prohibited |

Routine logs contain command, status code, counts, and revision only—never Asset
values. Evidence Reports contain aggregate counts and synthetic values only.
Fixtures are synthetic. Store, backups, and temporary files are Git-excluded and
support bundles exclude them unless an explicit local redaction workflow is
approved. No production Asset value may enter Git.

## Expected-availability foundation

Expected availability is future operator intent in the Asset layer, but it is
not a version 1.0 field and no values are approved here. A later versioned schema
migration may add a dedicated policy object after semantics for always-on,
scheduled, intermittent/transient, maintenance, and retirement are separately
approved.

That future checkpoint must define schedules/time zones, evidence freshness,
grace/debounce, authoritative active and HA observations, automation dependency
impact, maintenance overrides, incident thresholds, notification routing, and
privacy. Operational evaluation will compare current Observation against Asset
expectation without rewriting either, then provide derived incident evidence.
PE-2.1 creates only the durable stable-ID attachment point.

## PE-2.1 implementation package

1. **Strict Asset model and schemas**
   - Files: `pi4/lib/hioc/assets.py`, `tests/test_assets.py`.
   - Implement closed store/status validation, text normalization, deterministic
     serialization, stable-ID rules, orphan calculation, and sanitized errors.
   - No inventory, enrichment, identity, canonical, health, or public schema
     modification.
2. **Governed CLI and validator**
   - Files: `pi4/bin/hioc-assets.py`, `pi4/bin/hioc-validate-assets.py`.
   - Implement the approved commands, redaction defaults, dedicated locking,
     revision checks, backups, restore, and atomic writes.
3. **Release and operational integration**
   - Files: `pi4/install_pi4.sh`, `pi4/validate_pi4.sh`; release scripts only if
     tests prove current state/backup exclusions insufficient.
   - Make executables runnable; validate paired artifacts when initialized;
     preserve state/backups. Add no cron job or daemon.
4. **Evidence and documentation**
   - Files: `docs/PE2_ASSET_FOUNDATION_EVIDENCE.md` plus status updates to this
     specification, Master Plan, Operations, System Reference, Changelog and
     ADR-0019.
5. **Repository and production validation**
   - Focused matrix, full regression, privacy/secret review, deterministic
     serialization, protected payload comparisons, governed artifact identity,
     supported deployment, synthetic temporary Asset transaction, backup/restore,
     cleanup, and final pre-test semantic equality.

`pi4/lib/hioc/core/schemas.py` is not the preferred nested strict validator;
`assets.py` owns version-aware closed validation like PE-1. `core/state.py`
should remain unchanged unless implementation proves a missing generic atomic
primitive without changing existing callers. `inventory.py`, MQTT, HA,
dashboards, incidents, topology, services, and enrichment are out of scope.

## Required PE-2.1 test matrix

Implementation must cover:

1. Empty store and 2. one record; 3. multiple sorted records; 4. key/embedded-ID
agreement; 5. IP change survival; 6. hostname change survival; 7. canonical-IP
change survival; 8. temporary disappearance survival; 9. orphan preservation;
10. orphan count; 11. invalid ID; 12. unknown field; 13. missing version;
14. unsupported version; 15. empty friendly-name clear; 16. Unicode NFC;
17. control rejection; 18. duplicate names allowed; 19. physical-location
validation; 20. purpose validation; 21. notes maximum; 22. notes line/linebreak
rules; 23. atomic success; 24. atomic failure; 25. temporary cleanup;
26. concurrent lock; 27. lock timeout; 28. malformed existing store;
29. previous valid preservation; 30. pre-mutation backup; 31. backup validation;
32. restore validation; 33. file mode; 34. directory/backup modes;
35. public inventory unchanged; 36. MQTT unchanged; 37. HA unchanged;
38. dashboards unchanged; 39. incidents unchanged; 40. stable IDs unchanged;
41. canonical IP unchanged; 42. health unchanged; 43. liveness/observation
unchanged; 44. topology unchanged; 45. service ownership unchanged;
46. status online; 47. status degraded/error/unavailable semantics; 48. orphan
count consistency; 49. redaction/privacy; 50. synthetic fixtures only;
51. deterministic bytes; 52. strict cross-field schema; 53. full regression.

CLI tests additionally cover initialize; set/clear/remove; invalid input;
`--allow-orphan`; no-op timestamp/revision stability; expected-revision conflict;
backup failure; concurrent rejection; list/show redaction and explicit sensitive
display; path-safe restore; and sanitized output.

## Future production validation plan

Do not embed a PI3 command in this design. A later authorized operator procedure
must prove exact approved commit and Git-derived identities; clean source;
supported deployment and timestamped release backup; restrictive initialized
store/status; strict validation; dedicated-lock behavior; and bounded runtime.

Capture protected pre/post inventory, MQTT, HA input, dashboard, incident,
identity, canonical IP, health/liveness/observation, topology and service-owner
invariants. Create the reserved synthetic orphan through the CLI, prove
persistence across an inventory run, correct orphan count, invalid-write
rejection without byte change, backup creation, validated restore, and removal.
Final Asset store must semantically equal the pre-test store, and evidence must
contain no Asset values or secrets.

Outcomes:

- **PASS:** deployment/artifacts, write/backup/restore, cleanup, privacy and all
  protected invariants pass.
- **PARTIAL PASS:** deployment and protected invariants pass but an optional
  production observation is unavailable; no deterministic defect or privacy
  failure exists.
- **FAIL:** deterministic artifact/schema/write/backup/restore, stable identity,
  canonical IP, public contract, privacy, or bounded-runtime failure.

Rollback is justified only for deployed artifact mismatch, store/write
corruption, required backup/restore failure, stable-ID or canonical-IP regression,
public inventory/MQTT/HA/dashboard/incident regression, privacy exposure, or a
runtime failure affecting inventory. Empty stores, empty optional fields,
orphaning, allowed duplicate names, removed synthetic validation data, or absent
future fields are not rollback reasons.

## Explicit deferrals and stopping conditions

Deferred: owner, structured location, public projection/presentation resolver,
UI/API/HA editing, import/export, multi-identity physical Asset association,
identity alias/migration, operator authentication/`updated_by`, change reasons,
append-only audit history, automatic backup pruning, off-device backup transport,
lifecycle/retirement/archive, expected availability, criticality, maintenance,
permanent-IoT monitoring, HA association, automation impact, notifications,
incidents, manufacturer/OUI, classification, retention, and Active Discovery.

PE-2.1 must stop for any requirement to change identity, canonical address,
public inventory, current name/hostname/display behavior, MQTT, HA, dashboards,
incidents, health/liveness/observation, topology, service ownership, or any
deferred field or workflow. Those require separate authorization.
