# PE-4 Home Assistant Association Contract

## Authority and lifecycle

PE-4.0C PASS/CLOSED: repository-only contract freeze; no runtime adapter exists.
The [canonical contract](../governance/pe4/pe4-0c-association-contract.json),
[contract schema](../governance/pe4/pe4-0c-association-contract.schema.json) and
[private-state schema](../governance/pe4/pe4-home-assistant-association-state.schema.json)
are the machine-readable authority. Private state is future-only at
`state/inventory/associations/home_assistant.json`; no state is created here.

The accepted [2b closure](../governance/pe4/pe4-0b2b-execution-closure.json)
and operator-supplied sanitized production handoff bind report SHA-256
`322e237404c3c721be782e9ce2dbc4ceb1e63b8374af00b6fe75a940624d2ded`,
result SHA-256 `685606f76aad93ede32b52c2ffa34984408d62d408185ab6141791eded478e43`,
and structure fingerprint `fef567f29e545e1b7c03b4a8c585f0b03b6ea8b588c5502acb5ce51e809d9b1d`.
Private production evidence `/tmp/hioc-pe4-ha-discovery-7bb82b7c` was not accessed.
HA Core 2026.9.4 versus historical source baseline 2026.8.1 was COMPATIBLE_UPDATED,
failed capability null, likely update compatibility break false. This proves the
observed interface only, not universal future HA compatibility.

## October 6, 2026 production constraints

229 devices: 169 zero-MAC, 58 one-MAC, 2 multiple-MAC; 62 MAC entries,
54 canonical, 8 invalid, 9 colliding values across 18 HA devices. No arbitrary
repair or heuristic can turn those ambiguities into automatic associations.
2425 entities: 2241 with device membership and 184 without; 22 areas and
97 config entries. Template 52, scene 5, automation 61, group 0 are structural
classifications, not physical identity. Additive unknown fields and 177 unpublished
namespace occurrences remain count/type-only. Unknown names are not invented.
Counts describe this snapshot and are not permanent expected counts.

## State validation and publication boundary

The schema is closed at every object, bounds arrays and strings, permits only
strong associations, and uses HIOC stable device ID as the canonical reference.
Private HA relationship keys and selected source metadata are permitted only
within their allowlists. Unique ID, raw MAC, IP, hostname, serial, configuration
URL, config-entry title, raw responses and arbitrary namespaces are excluded.
No private registry identifiers or household descriptive values belong in public
inventory, MQTT or ordinary logs. The public projection allowlist is associated,
association_basis, entity_count, safe integration_domains and has_area_candidate;
its implementation is deferred. Private basis `unique_mac` projects as `strong_mac`.

JSON Schema checks shape, bounds and whole-item duplication; future adapter
validation must additionally enforce uniqueness of HIOC and HA keys, timestamp
ordering, referential membership, summary consistency and prior-binding constraints.
These cross-record semantic checks are mandatory before atomic publication.
Per-record review/rejection outcomes belong to bounded count-only diagnostics,
not to an alternative identity record. Invalid input or publication failure keeps
last-known-good state; a prior conflict never silently moves a durable binding.

## Existing authority rules that PE-4.0C must preserve

The existing access/privacy contract already establishes:

### Strong candidate

Exact normalized HA **device MAC connection** matching exactly one existing MAC-backed HIOC identity.

### Supporting only

Examples include:

- integration-specific identifiers;
- IP corroboration after a strong identity is already established;
- hostname;
- manufacturer;
- model;
- config-entry ownership;
- HA device name;
- HA area.

### Weak / reviewable only

Examples include:

- IP-only match;
- hostname-only match;
- name similarity;
- area similarity;
- manufacturer/model similarity.

### Never independent identity

Examples include:

- friendly name;
- entity ID;
- entity unique ID;
- HA area;
- manufacturer/model;
- availability/state;
- helper;
- template;
- group;
- scene;
- automation;
- entity without physical HA device identity;
- conflicting MAC evidence.

HIOC remains authoritative for:

- stable HIOC device ID;
- canonical MAC identity;
- canonical IP;
- passive observation;
- liveness;
- health;
- incidents;
- expected availability.

Home Assistant is authoritative only for its own registry metadata.

Operator Asset knowledge remains highest authority for descriptive human-managed metadata.

HA must never overwrite an operator Asset field.

## Critical PE-4.0C decision: “MAC exists” is NOT sufficient

The live evidence proves that Home Assistant contains:

- invalid MAC entries;
- devices with multiple MAC entries;
- duplicated MAC values across multiple HA devices;
- many devices with no MAC.

Therefore freeze the following rule.

An HA device qualifies for automatic strong association only when **all** of the following are true:

1. The record is a valid HA device-registry record under the frozen structural contract.
2. Its `connections` field can be safely parsed under the reviewed pair-array model.
3. It contains the `mac` connection namespace.
4. Every `mac` connection value considered for association is structurally valid.
5. Exactly **one distinct valid normalized MAC** remains for that HA device.
6. The HA device has no invalid or ambiguous MAC condition that makes its physical identity uncertain.
7. That normalized MAC occurs on exactly **one HA device** in the complete device-registry snapshot used for that association cycle.
8. The normalized MAC matches exactly **one existing canonical MAC-backed HIOC device**.
9. No conflicting HIOC canonical identity exists.
10. No prior durable HA-device-to-HIOC association conflicts with the new proposed binding.
11. The operation does not require changing the HIOC stable ID, MAC or canonical IP.
12. The association can be represented without turning HA into a discovery/liveness source.

Only then classify:

`ASSOCIATED_STRONG_MAC`

## Global snapshot requirement for MAC collision detection

Future implementation must not decide association record-by-record before knowing whether a MAC is duplicated elsewhere in the HA snapshot.

It must first build bounded in-memory indexes sufficient to determine:

- normalized MACs by HA device;
- HA devices by normalized MAC;
- invalid MAC conditions;
- multiple-MAC conditions;
- HIOC devices by normalized canonical MAC.

Only after global uniqueness is known may strong association decisions be made.

This is required because production already showed:

```text
mac_collision_values = 9
mac_conflicting_devices = 18
```

Do not select one of several HA devices sharing the same MAC.

Do not use ordering, first match, name similarity, config entry, integration domain, area, manufacturer, model or entity count as a tiebreaker.

## Multiple MAC rule

If an HA device contains more than one distinct valid normalized `mac` connection:

Do not automatically select one.

Classification:

`REVIEW_ONLY_MULTIPLE_MAC`

Even if one of those MACs happens to match a HIOC device.

A later separately governed rule may support explicit multi-interface devices.

PE-4.0C does not.

## Invalid MAC rule

If an HA device's MAC evidence is malformed or cannot be normalized under the HIOC canonical MAC contract:

It cannot produce an automatic strong association from that evidence.

Classification:

`REJECT_INVALID_MAC`

Do not attempt to repair arbitrary MAC-like data beyond the already governed normalization forms.

Do not derive a MAC from:

- Bluetooth identifiers;
- UPnP identifiers;
- entity IDs;
- unique IDs;
- serial numbers;
- names;
- configuration URLs;
- arbitrary integration identifiers.

## HA MAC collision rule

If one normalized MAC is present on more than one HA device record:

Every affected automatic association must fail closed.

Classification:

`REJECT_HA_MAC_COLLISION`

Do not choose the first record.

Do not select by config entry.

Do not select by entity count.

Do not select by device name.

Do not select by area.

Do not select by manufacturer/model.

Do not silently associate multiple HA devices to one HIOC canonical identity.

A future operator-approved multi-registry-device model may be designed separately.

## HIOC-side ambiguity rule

Future adapter must not assume HIOC invariants without verifying them at the association boundary.

If one normalized MAC corresponds to more than one current HIOC canonical device:

Classification:

`REJECT_HIOC_MAC_AMBIGUITY`

Do not merge the HIOC devices.

Do not change stable IDs.

Do not repair inventory identity inside PE-4.

This condition is an upstream HIOC identity-invariant problem and should be surfaced as such.

## Unmatched valid MAC

If HA has one valid globally unique normalized MAC but no existing HIOC canonical MAC-backed device has that MAC:

Classification:

`UNMATCHED_STRONG_EVIDENCE`

PE-4 must **not create a new HIOC device**.

PE-4 is an association layer over an already-reconciled inventory.

It is not a new discovery source.

This record may contribute only to aggregate/private review diagnostics.

## No-MAC devices

The live snapshot contains:

`169`

HA devices with no MAC connection.

No-MAC records must never be automatically associated from weaker fields.

Classification:

`REVIEW_ONLY_NO_MAC`

Potential supporting information may exist, but automatic identity is prohibited.

Do not auto-associate from:

- name;
- name_by_user;
- area;
- manufacturer;
- model;
- serial number;
- config entry;
- integration domain;
- identifiers;
- entity membership;
- entity count;
- hostname-like text;
- UPnP;
- Bluetooth;
- MQTT identifier;
- Hue identifier;
- Z-Wave identifier.

## Connection namespaces

Freeze namespace authority as follows.

## `mac`

Only currently approved strong-identity namespace.

Subject to all uniqueness and conflict rules above.

## `bluetooth`

Not canonical HIOC network-device identity authority.

Supporting/private metadata only if later explicitly needed.

Do not reinterpret a Bluetooth address as HIOC canonical Ethernet/Wi-Fi MAC identity.

## `upnp`

Supporting/private relationship metadata only.

Never independent identity.

Do not infer canonical IP, hostname or MAC from arbitrary UPnP connection values unless a future separately reviewed contract defines an exact safe shape.

## Unknown or unpublished namespaces

Never identity authority.

Ignore values for current PE-4 association.

They may contribute only bounded aggregate diagnostics.

The production snapshot contained `177` unpublished namespace occurrences, so this rule is operationally relevant, not hypothetical.

Adding a new namespace to identity authority requires a future explicit contract update.

## Identifier namespaces

Observed allowlisted identifier namespaces:

```text
hue
mqtt
upnp
zwave_js
```

These are **not HIOC stable identity authority**.

They may be used only as Home Assistant-owned supporting metadata after an association is already independently established.

Do not use an integration-specific identifier to create, merge or select a HIOC identity.

Unknown identifier namespaces receive no authority.

## IP boundary

The live frozen device registry does not expose a reviewed generic top-level IP field.

Therefore the future PE-4 adapter must not invent an IP extractor from:

- UPnP connection values;
- identifiers;
- configuration URL;
- name;
- serial number;
- device metadata.

The existing conceptual rule that IP can corroborate an already established MAC match remains true, but the current frozen HA schema supplies no approved generic IP extraction contract.

Therefore current PE-4 implementation has:

`HA_IP_IDENTITY_EXTRACTION = NOT_AUTHORIZED`

Any future IP extraction requires separate review.

## Hostname boundary

No dedicated reviewed hostname field was observed in the HA device schema.

Therefore:

- `name` is not a hostname;
- `name_by_user` is not a hostname;
- entity IDs are not hostnames;
- configuration URLs must not be parsed for hostnames.

Current PE-4 implementation has:

`HA_HOSTNAME_IDENTITY_EXTRACTION = NOT_AUTHORIZED`

## Device registry relationship authority

HA device `id` is a private HA registry relationship key.

It is authoritative only inside the HA association model.

It must never replace the HIOC device ID.

Once strong association exists, the private HA device ID may be retained locally to maintain the HA relationship.

`config_entry_id`, `config_entries`, `config_entries_subentries`,
`config_subentry_id`, `primary_config_entry`, and `via_device_id` are HA-owned relationship metadata.

They are not HIOC identity authority.

`via_device_id` must not directly change HIOC network topology in PE-4.

It may be preserved as a future HA topology candidate only.

## Entity membership rule

Entities may be associated with a HIOC device only through:

`entity.device_id -> strongly associated HA device -> HIOC device`

An entity must never independently select a HIOC identity.

Production contains:

```text
2241 entities with device
184 entities without device
```

The 184 entities without HA device membership cannot create physical-device associations.

Classify them as:

`ENTITY_WITHOUT_DEVICE_IDENTITY`

They may remain HA-only metadata.

Do not map them by entity ID, unique ID, area, platform, name or integration.

## Template, scene, group and automation rule

Observed production counts include:

```text
template = 52
scene = 5
automation = 61
group = 0
```

These categories must never create HIOC device identity.

They may be useful in PE-8 functional-impact work later.

PE-4.0C must preserve that boundary.

Do not move PE-8 work into PE-4.

## Entity IDs and unique IDs

`entity_id`, entity-registry `id`, and `unique_id` are Home Assistant-private identifiers.

They must never become HIOC stable identity keys.

For future PE-4 implementation:

- private local retention of entity relationship references may be permitted only inside the dedicated HA association state;
- they must not be written into the ordinary public inventory identity fields;
- they must not be MQTT-published by default;
- they must not appear in ordinary logs;
- they must not become matching authority.

`unique_id` specifically must not be used as independent cross-system physical identity.

## Config-entry authority

Config entries provide integration ownership/context only.

Production contains:

`97`

config entries.

Do not use:

- `entry_id`;
- `domain`;
- `title`;
- `source`;
- `state`;
- disabled status;

as independent HIOC identity evidence.

Integration domain may be retained as technical metadata after a strong association.

Config-entry title is household metadata and must not be published by default.

Config-entry IDs remain private relationship keys.

## Area authority

HA areas are descriptive candidates only.

Production contains:

`22`

areas.

HA area must never:

- create identity;
- merge identities;
- alter HIOC canonical IP;
- alter HIOC MAC;
- replace an operator Asset `physical_location`.

Operator-managed Asset metadata has higher descriptive authority.

If future PE-4 implementation retains HA area, it must remain clearly source-specific, for example conceptually:

`home_assistant.area_candidate`

not:

`asset.physical_location`

No implicit promotion is permitted.

## Device naming authority

`name` and `name_by_user` belong to Home Assistant registry metadata.

They may be retained as HA-specific descriptive metadata.

They must never overwrite:

- Asset `friendly_name`;
- HIOC canonical hostname;
- stable HIOC ID.

No fuzzy name matching is authorized.

## Manufacturer/model authority

HA manufacturer/model/hardware/software metadata is supporting descriptive evidence only.

It cannot override:

- operator Asset metadata;
- governed manufacturer enrichment;
- existing stronger source authority.

Do not use manufacturer/model similarity to auto-associate devices.

If retained, preserve source provenance as Home Assistant metadata.

## Serial-number boundary

The live schema exposes `serial_number`.

PE-4.0C does **not** approve serial number as independent HIOC identity.

Do not automatically persist or expose it.

Do not use it for automatic matching.

Any future use requires separate privacy and identity review.

## Configuration URL boundary

`configuration_url` may contain sensitive or network-specific information.

Do not use it for identity.

Do not persist it in PE-4 association state.

Do not log it.

Do not publish it.

Do not extract hostname/IP from it.

## Labels/icons/pictures/options/categories

The following do not influence identity:

- labels;
- icons;
- pictures;
- options;
- categories;
- translation keys;
- aliases.

Do not use them as automatic association evidence.

## Required association cardinality

Current automatic PE-4 strong association is strictly:

**one HA device registry record ↔ one existing HIOC canonical device**

One HIOC device may have many HA entities through that one HA device.

Automatic many-HA-device-to-one-HIOC-device association is not approved.

Automatic one-HA-device-to-many-HIOC-device association is not approved.

Future support for those cases requires explicit architecture.

## Prior-binding conflict rule

If a future durable association already binds:

`HA device X -> HIOC device A`

and a later snapshot would bind the same HA device to:

`HIOC device B`

do not silently move the association.

Classification:

`REJECT_PRIOR_BINDING_CONFLICT`

Retain the previous known-good association separately from the conflicting observation.

Surface review-required diagnostics.

This protects against:

- HA registry reconstruction;
- MAC changes;
- device replacement;
- data corruption;
- HIOC identity change;
- accidental cross-device association.

## Association reason vocabulary

Freeze at least these machine-readable outcomes:

```text
ASSOCIATED_STRONG_MAC
REVIEW_ONLY_NO_MAC
REVIEW_ONLY_MULTIPLE_MAC
REJECT_INVALID_MAC
REJECT_HA_MAC_COLLISION
REJECT_HIOC_MAC_AMBIGUITY
REJECT_PRIOR_BINDING_CONFLICT
UNMATCHED_STRONG_EVIDENCE
ENTITY_WITHOUT_DEVICE_IDENTITY
```

REJECT_STRUCTURAL_CONTRACT covers invalid required record shapes; no fuzzy confidence scores or heuristic matching are permitted.

No percentage confidence model is authorized.

## Critical architecture boundary: do not use generic integration ingestion

The current HIOC inventory code has a generic integration input under:

`state/inventory/integrations`

and generic integration records can participate in inventory identity construction.

PE-4 must **not** implement Home Assistant association by simply writing HA device records into that existing generic integration-device input.

Reason:

PE-4 is not a new identity/discovery engine.

Using generic integration ingestion could accidentally:

- create a new HIOC identity;
- promote HA data into identity authority;
- affect source precedence;
- mark records as observed;
- influence last-seen/liveness;
- alter operational-monitoring semantics;
- change health/incidents.

Freeze this prohibition explicitly.

Home Assistant association requires a **dedicated post-identity association layer**, not generic inventory discovery ingestion.

## Dedicated private association state

Freeze a dedicated association-state concept separate from generic inventory discovery.

Preferred path:

`state/inventory/associations/home_assistant.json`

The frozen path is under the dedicated `associations` boundary and never under generic `integrations` discovery ingestion.

This file is future runtime state.

Do not create production state now.

PE-4.0C should define its schema/contract only.

## Private association-state authority

Future private HA association state may contain, after strong association:

- HIOC stable device ID;
- approved instance reference `PI5_HA`;
- private HA device-registry ID;
- association basis `unique_mac`;
- association status;
- first-associated timestamp;
- last-confirmed timestamp;
- observed HA Core version;
- source/contract version;
- selected HA-owned descriptive metadata;
- private entity membership references;
- selected integration ownership metadata;
- selected HA area candidate;
- bounded diagnostic state.

The private association state must not contain a second authoritative HIOC MAC/IP identity.

Raw HA MAC may be processed in memory for matching but should not need to be duplicated into durable association state because the matched HIOC device already owns the canonical MAC.

## Private retained entity relationships

Because HA is authoritative for entity membership, the frozen private association state may retain entity relationship references for entities belonging to a strongly associated HA device.

Permitted private fields may include only what is necessary for association and future governed correlation, such as:

- entity registry ID;
- entity ID;
- platform;
- config-entry relationship;
- disabled status;
- entity category;
- HA area relationship.

Retaining `unique_id` requires a separate necessity and privacy contract review.

Default decision should be:

`unique_id = NOT_RETAINED`

These private entity references must not be exposed in the public inventory or MQTT by PE-4.0C.

## Private integration ownership metadata

After strong device association, private HA association state may retain bounded integration ownership metadata such as:

- integration domain;
- private config-entry relationship;
- disabled/state classification where useful.

Do not use it for identity.

Do not expose config-entry title by default.

Do not interpret config-entry state as HIOC device liveness.

## Public projection boundary

Freeze a separate public-safe projection.

The ordinary HIOC inventory must not expose raw HA registry IDs, entity IDs, unique IDs, config-entry IDs, device names, area names or private registry relationship values unless a later schema explicitly authorizes them.

Future public inventory enrichment may safely expose bounded association facts such as:

```text
home_assistant.associated = true
home_assistant.association_basis = strong_mac
home_assistant.entity_count = integer
home_assistant.integration_domains = safe technical domain list
home_assistant.has_area_candidate = boolean
```

Exact public schema implementation is a later implementation checkpoint.

PE-4.0C must freeze the privacy distinction now.

## Asset precedence

Freeze precedence:

1. Operator Asset metadata
2. Existing HIOC canonical discovered/known identity according to its field authority
3. Governed manufacturer enrichment according to its existing contract
4. Home Assistant descriptive metadata as source-specific supporting evidence

Home Assistant must never overwrite operator Asset:

- friendly name;
- physical location;
- purpose;
- notes;
- future owner/criticality/expected-availability fields.

## Observation and liveness boundary

Home Assistant association must not:

- create `last_seen`;
- refresh `last_seen`;
- set `reachable`;
- set offline/online;
- alter observation status;
- alter operational-monitoring policy;
- create availability incidents;
- close availability incidents;
- change health score;
- change health status.

PE-7 and PE-10 will separately govern availability/integration/service-health semantics.

Do not pull that work into PE-4.

## Do not add Home Assistant to current generic source provenance in a way that changes monitoring

The current inventory monitoring behavior depends partly on discovery/source provenance.

Therefore future PE-4 association must not casually append a generic discovery source such as `integration:home_assistant` to current identity records if that would change observation, monitoring or health semantics.

HA association provenance must live in its own association namespace/state.

Any future decision to make HA an operational observation source requires a separate checkpoint.

## Transactional publication requirement

Future adapter implementation must compute candidate association state in memory first.

Before replacing last-known-good association state it must validate:

- complete required registry reads;
- compatibility contract;
- record shape;
- MAC parsing;
- global HA MAC uniqueness;
- HIOC MAC uniqueness;
- prior-binding conflicts;
- private-state schema;
- privacy/public projection constraints.

Only a completely validated candidate state may atomically replace current association state.

On:

- transport failure;
- authentication failure;
- schema incompatibility;
- required command failure;
- compatibility failure;
- state-publication failure;

retain last-known-good association state.

Do not erase associations merely because Home Assistant is temporarily unavailable.

## Additive schema evolution

Production already showed:

- unknown device fields;
- unknown config-entry fields;
- unpublished namespaces.

Therefore freeze:

Unknown additive fields are tolerated only when all required fields and required types remain compatible.

Unknown fields:

- are not consumed;
- are not retained;
- do not become identity;
- may be counted diagnostically.

Unknown namespaces:

- do not become identity;
- are ignored for matching until separately reviewed.

If a required field disappears or changes incompatibly, the HA association subsystem must fail closed through the compatibility architecture.

## Required structural inputs for association implementation

Freeze the smallest required device-level structural core for strong association.

At minimum:

```text
device.id           string
device.connections  array
```

The adapter may additionally consume reviewed metadata fields only under their frozen authority.

Do not make every field observed in 2026.9.4 globally mandatory merely because it happened to be present in every current record.

Use source-reviewed type contracts plus live evidence to distinguish:

- association-required fields;
- optional metadata;
- relationship fields;
- ignored fields.

This is essential for compatibility resilience.

## Entity structural core

For private entity membership after strong device association, freeze at minimum:

```text
entity.device_id   null|string
entity.entity_id   string
entity.id          string
entity.platform    string
```

Additional fields are optional source-specific metadata.

Entity `unique_id` is not identity authority and should not be retained by default.

## Area structural core

For source-specific area metadata:

```text
area.area_id  string
area.name     string
```

Area metadata is optional association enrichment only.

It does not affect identity.

## Config-entry structural core

For source-specific integration ownership:

```text
config_entry.entry_id  string
config_entry.domain    string
```

Other fields may be consumed only if specifically useful under the frozen contract.

Config-entry title is not required.

## Disabled records

A disabled HA device/entity/config entry is still registry metadata.

Disabled status must not silently invalidate an otherwise valid HIOC identity.

For PE-4 association:

- disabled may be retained as HA metadata;
- disabled does not create or destroy HIOC identity;
- disabled does not prove offline state.

Do not infer liveness.

## `via_device_id`

`via_device_id` is HA relationship metadata.

It may later support topology correlation only after both HA devices are independently and strongly associated.

PE-4.0C must not authorize it to:

- create HIOC identity;
- merge HIOC devices;
- rewrite network parent topology.

PE-9 owns broader technical dependency/topology intelligence.

## Snapshot consistency

The four HA registry reads are sequential and are not a transactional Home Assistant snapshot.

Therefore future implementation must not claim cross-registry atomicity.

Device-level MAC association may be based on the internally consistent device-registry response.

Entity/area/config-entry relationship metadata should be treated as best-effort within the completed bounded invocation.

Dangling cross-registry references must not fabricate relationships.

If relationship completeness is materially uncertain, retain the strong device association but mark relationship metadata incomplete rather than inventing links.

## Compatibility integration

Future PE-4 association adapter must consume the project compatibility model.

A version change alone must not stop association.

Compatible version drift:

`COMPATIBLE_UPDATED`

Required interface/schema failure:

appropriate compatibility failure for the HA association subsystem.

A compatibility failure must not make DHCP, NUT, inventory, manufacturer, MQTT, or unrelated HIOC functions appear globally broken.

## No mutation authority

PE-4 remains read-only toward Home Assistant.

The association adapter must never:

- write HA registry entries;
- rename devices;
- change areas;
- change entities;
- reload integrations;
- call mutation services;
- modify configuration;
- restart HA;
- modify `.storage`;
- write states;
- execute automations.

Association is consumption only.


## No fuzzy matching

Explicit regression protection must prevent future accidental introduction of automatic matching by:

- Levenshtein/string similarity;
- substring name matching;
- manufacturer/model scoring;
- area scoring;
- entity-count scoring;
- integration-domain scoring;
- weighted confidence percentages.

PE-4.0C authorizes deterministic strong association only.

## No automatic reconciliation from HA duplicates

Do not use HA duplicate device records to merge HIOC identities.

HA duplicates remain an HA association ambiguity.

HIOC identity stays unchanged.

## No assumption that 229 HA devices equal HIOC devices

HA registry count and HIOC inventory count are different domains.

Do not compare totals as if coverage should be 1:1.

Do not create missing HIOC identities merely to close the count gap.

## No assumption that all physical devices have HA entities

Absence from Home Assistant does not reduce confidence in a HIOC device.

Home Assistant association is optional enrichment.

## No assumption that HA entity presence proves device availability

Entity registry membership is configuration metadata.

It does not prove the entity or physical device is currently functioning.

PE-7/PE-10 own those semantics later.


## Sanitized observed structure appendix

Recognized fields/types and counts below are operator-supplied snapshot facts.
Observed presence never makes optional metadata universally required.

```json
{
  "area_registry": {
    "counts": {
      "total": 22
    },
    "recognized_fields_types": {
      "aliases": [
        "array"
      ],
      "area_id": [
        "string"
      ],
      "created_at": [
        "number"
      ],
      "floor_id": [
        "null"
      ],
      "humidity_entity_id": [
        "null"
      ],
      "icon": [
        "null",
        "string"
      ],
      "labels": [
        "array"
      ],
      "modified_at": [
        "number"
      ],
      "name": [
        "string"
      ],
      "picture": [
        "null"
      ],
      "temperature_entity_id": [
        "null"
      ]
    }
  },
  "config_entry_registry": {
    "counts": {
      "disabled": 1,
      "total": 97,
      "unknown_field_occurrences": 97
    },
    "recognized_fields_types": {
      "created_at": [
        "number"
      ],
      "disabled_by": [
        "null",
        "string"
      ],
      "domain": [
        "string"
      ],
      "entry_id": [
        "string"
      ],
      "error_reason_translation_key": [
        "null"
      ],
      "error_reason_translation_placeholders": [
        "null"
      ],
      "modified_at": [
        "number"
      ],
      "num_subentries": [
        "integer"
      ],
      "pref_disable_new_entities": [
        "boolean"
      ],
      "pref_disable_polling": [
        "boolean"
      ],
      "reason": [
        "null"
      ],
      "source": [
        "string"
      ],
      "state": [
        "string"
      ],
      "supported_subentry_types": [
        "object"
      ],
      "supports_options": [
        "boolean"
      ],
      "supports_reconfigure": [
        "boolean"
      ],
      "supports_remove_device": [
        "boolean"
      ],
      "supports_unload": [
        "boolean"
      ],
      "title": [
        "string"
      ]
    }
  },
  "device_registry": {
    "counts": {
      "connection_collision_values": 11,
      "connections_multiple": 6,
      "connections_one": 57,
      "connections_zero": 166,
      "disabled": 2,
      "identifier_collision_values": 0,
      "mac_canonical": 54,
      "mac_collision_values": 9,
      "mac_conflicting_devices": 18,
      "mac_duplicate_entries": 0,
      "mac_entries": 62,
      "mac_invalid": 8,
      "mac_multiple": 2,
      "mac_normalization_required": 0,
      "mac_one": 58,
      "mac_zero": 169,
      "total": 229,
      "unknown_field_occurrences": 229,
      "unpublished_namespace_occurrences": 177,
      "via_device": 19,
      "with_area": 58,
      "with_config_entry": 229
    },
    "recognized_fields_types": {
      "area_id": [
        "null",
        "string"
      ],
      "config_entries": [
        "array"
      ],
      "config_entries_subentries": [
        "object"
      ],
      "config_entry_id": [
        "string"
      ],
      "config_subentry_id": [
        "null",
        "string"
      ],
      "configuration_url": [
        "null",
        "string"
      ],
      "connections": [
        "array"
      ],
      "created_at": [
        "number"
      ],
      "disabled_by": [
        "null",
        "string"
      ],
      "entry_type": [
        "null",
        "string"
      ],
      "hw_version": [
        "null",
        "string"
      ],
      "id": [
        "string"
      ],
      "identifiers": [
        "array"
      ],
      "labels": [
        "array"
      ],
      "manufacturer": [
        "null",
        "string"
      ],
      "model": [
        "null",
        "string"
      ],
      "model_id": [
        "null",
        "string"
      ],
      "modified_at": [
        "number"
      ],
      "name": [
        "null",
        "string"
      ],
      "name_by_user": [
        "null",
        "string"
      ],
      "primary_config_entry": [
        "string"
      ],
      "serial_number": [
        "null",
        "string"
      ],
      "sw_version": [
        "null",
        "string"
      ],
      "via_device_id": [
        "null",
        "string"
      ]
    }
  },
  "entity_registry": {
    "counts": {
      "automation_domain": 61,
      "disabled": 1042,
      "group_domain": 0,
      "scene_domain": 5,
      "template_platform": 52,
      "total": 2425,
      "with_area": 1,
      "with_config_entry": 2291,
      "with_device": 2241,
      "without_device": 184
    },
    "recognized_fields_types": {
      "area_id": [
        "null",
        "string"
      ],
      "categories": [
        "object"
      ],
      "config_entry_id": [
        "null",
        "string"
      ],
      "config_subentry_id": [
        "null",
        "string"
      ],
      "created_at": [
        "number"
      ],
      "device_id": [
        "null",
        "string"
      ],
      "disabled_by": [
        "null",
        "string"
      ],
      "entity_category": [
        "null",
        "string"
      ],
      "entity_id": [
        "string"
      ],
      "has_entity_name": [
        "boolean"
      ],
      "hidden_by": [
        "null",
        "string"
      ],
      "icon": [
        "null",
        "string"
      ],
      "id": [
        "string"
      ],
      "labels": [
        "array"
      ],
      "modified_at": [
        "number"
      ],
      "name": [
        "null",
        "string"
      ],
      "options": [
        "object"
      ],
      "original_name": [
        "null",
        "string"
      ],
      "platform": [
        "string"
      ],
      "translation_key": [
        "null",
        "string"
      ],
      "unique_id": [
        "string"
      ]
    }
  }
}
```
