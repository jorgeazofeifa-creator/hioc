# PE-4 Home Assistant Association Lifecycle Clarification

## Authority and scope

PE-4.0C.1 is PASS/CLOSED after repository-only validation. It supplements the
[frozen 0C authority](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md); the original
[canonical contract](../governance/pe4/pe4-0c-association-contract.json) and
[private-state schema 1.0](../governance/pe4/pe4-home-assistant-association-state.schema.json)
retain their exact bytes. Their SHA-256 identities are respectively
`a48ec696c7e596dde68e252366f84ea46dfa7076a9b1aaff419a993742ed9a58` and
`0a85d0e16f8d27f6532846e00eed843915b06ed2a3b84fd74285d931f3e6892d`.

The [clarification record](../governance/pe4/pe4-0c1-association-lifecycle-clarification.json)
and [record schema](../governance/pe4/pe4-0c1-association-lifecycle-clarification.schema.json)
freeze these additional lifecycle rules. Future implementation must use
[private-state schema 1.1](../governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json)
at the unchanged future path `state/inventory/associations/home_assistant.json`.
The stopped implementation-preparation review correctly made no changes: 0C
left successful-snapshot withdrawal and registry-ID continuity unspecified.
This task resolves that gap; it does not resume implementation preparation.

No adapter or production association state exists. No production migration,
credential design, writer implementation or deployment occurs here.

## Failed acquisition versus successful complete cycle

Acquisition, authentication, required-command, compatibility, schema,
canonical-inventory-input, candidate-validation and publication failures retain
the entire last-known-good private state unchanged. Failed reads cannot be
interpreted as empty registries or disappearance. No partial candidate, empty
fallback, failed diagnostics or newly retired history replaces valid prior state.

A successfully completed cycle publishes only strong associations reconfirmed
by that cycle. A previously strong pair that cannot be reconfirmed moves out of
active `associations` and into private `binding_history`. Other valid associations
may continue to publication. Retiring one pair is not an acquisition failure.
The successful candidate must validate active records, history, history changes,
uniqueness, prior bindings, summaries, privacy and atomic replacement as a whole.

The original UNIQUE_VALID_NONCOLLIDING_MAC rule is unchanged: exactly one distinct
valid normalized MAC per HA device, no invalid evidence, global HA uniqueness,
exactly one existing canonical MAC-backed HIOC identity, and no conflict. History
cannot pick a winner among collisions or supply missing current MAC evidence.

## Current associations and historical safety memory

Schema version 1.1 retains the closed active array and adds required, closed,
bounded `binding_history`. Active records still have status ASSOCIATED_STRONG_MAC.
They describe the current successful cycle only, with one HA ID per HIOC ID and
one HIOC ID per HA ID. Only active records may feed future `associated=true`
projection. Public projection implementation remains deferred.

History records contain exactly HIOC stable ID, private HA device ID,
first_associated_at, last_confirmed_at, retired_at and retirement_reason. No MAC,
IP, hostname, entity/unique/config-entry IDs, names, serial, URL, raw values or
credential is allowed. History is private relationship safety memory; it does
not create/resurrect a HIOC device or become identity, liveness, health, Asset
history, public inventory, logs or MQTT content.

A retired episode can coexist with a later reactivated active record of the same
pair: the historical episode remains past, never a second current association.
Across both arrays, a given HA registry ID may target only one HIOC stable ID.
Attempting a different target is REJECT_PRIOR_BINDING_CONFLICT, including when
the old pair exists only in history. No conflict is recorded as a completed rebind.

## Successful-snapshot disposition table

| Current successful observation of a prior active pair | Active candidate | Historical retirement reason / current outcome |
| --- | --- | --- |
| Same HA ID and HIOC ID satisfy the full strong rule | Reconfirm; retain exact pair first timestamp | No retirement; ASSOCIATED_STRONG_MAC |
| HA ID absent from complete device response | Remove prior pair | HA_DEVICE_ABSENT |
| HA ID has no MAC evidence | Remove prior pair | HA_DEVICE_NO_MAC; REVIEW_ONLY_NO_MAC |
| HA MAC evidence invalid, including valid plus invalid entries | Remove prior pair | HA_DEVICE_INVALID_MAC; REJECT_INVALID_MAC |
| More than one distinct valid normalized MAC | Remove prior pair | HA_DEVICE_MULTIPLE_MAC; REVIEW_ONLY_MULTIPLE_MAC |
| HA MAC is duplicated across current HA devices | Remove all affected prior pairs | HA_DEVICE_MAC_COLLISION; REJECT_HA_MAC_COLLISION |
| Successfully read canonical inventory lacks old HIOC ID | Remove prior pair | HIOC_DEVICE_ABSENT; never recreate HIOC identity |
| Old HIOC ID remains but canonical MAC differs from current HA MAC | Remove prior pair | HIOC_CANONICAL_MAC_NO_LONGER_MATCHES; a proposed other HIOC target is REJECT_PRIOR_BINDING_CONFLICT |
| Current canonical MAC maps ambiguously to multiple HIOC records | Remove affected prior pair | HIOC_MAC_AMBIGUITY; REJECT_HIOC_MAC_AMBIGUITY |
| Safe HA ID recreation satisfies every condition below | Replace old pair with new pair | HA_DEVICE_RECREATED; new exact-pair first timestamp |
| Device identity reconfirmed but relationship metadata incomplete | Keep strong active pair | relationship_status INCOMPLETE; no retirement |

Missing/unreadable/malformed/structurally invalid canonical inventory is an input
failure, not the successful HIOC_DEVICE_ABSENT case: retain the entire prior
state. Valid per-MAC ambiguity remains the existing 0C fail-closed outcome.
None of these cases changes HIOC identity, MAC, IP, observations, liveness,
health, incidents or operator Asset fields.

For simultaneous reasons, apply deterministic precedence: HA absent; invalid MAC;
no MAC; multiple MAC; HA collision; HIOC absent; HIOC MAC ambiguity; canonical
MAC mismatch. A validated safe recreation overrides HA_DEVICE_ABSENT with
HA_DEVICE_RECREATED. The extra bounded HIOC_MAC_AMBIGUITY retirement reason
covers the existing 0C ambiguity outcome without retaining a falsely active pair.
Current rejection diagnostics and retirement history are distinct domains.

## Reactivation and safe registry-ID recreation

The same historical HA ID may reactivate only when complete current strong
validation points to its same historical HIOC stable ID. Preserve the earliest
first_associated_at for that exact pair; advance last_confirmed_at only on
successful reconfirmation. A historical HA ID never automatically changes HIOC
target, regardless of current MAC evidence.

A new HA ID can replace a previously strong old HA ID only if all ten conditions
hold together:

1. The old pair was strongly bound to HIOC device A.
2. The old HA ID is absent from the complete current HA device response.
3. The new HA ID has exactly one distinct valid normalized MAC and no invalid evidence.
4. That MAC is globally unique in the complete current HA response.
5. It maps to exactly one canonical HIOC device.
6. That device is the same stable HIOC device A.
7. The new HA ID has no history pointing to another HIOC identity.
8. No other current active HA association targets A.
9. No competing current HA device has that MAC.
10. There is no HIOC-side MAC ambiguity.

Use the prior active pair as the replacement source. If there is no prior active
pair, use the most recent historical pair for A by last_confirmed_at. Tied
latest timestamps for different HA IDs require review rather than ordering or
name heuristics. The replacement source must be absent. A source HA ID still
present, a new ID previously bound elsewhere, or a current competing binding
blocks automatic replacement. Current MAC collisions always reject all affected
matches; history is never a tiebreaker.

Move the old binding to history with HA_DEVICE_RECREATED. If it was already
retired, preserve that original episode and its reason; do not rewrite past
history as a later recreation. Current-cycle recreation is captured by the
count-only HA_DEVICE_ID_RECREATED diagnostic. Give a never-before-bound new
HA-ID/HIOC-ID pair a new first_associated_at equal to this successful cycle's
publication time; never copy the old HA pair's timestamp. If the proposed HA ID
already belonged to A, that is same-pair reactivation, governed by the preceding
paragraph rather than a newly created pair.

## Deterministic history and capacity

The history limit is 4096 retirement episodes, with substantial headroom above
the observed 229-device snapshot. Never silently evict, compact away safety
pairs, or forget an HA-ID target to make room. If any new required retirement
cannot fit, emit BINDING_HISTORY_CAPACITY_EXCEEDED, publish nothing and preserve
the entire last-known-good state. Archival/retention policy is separate future work.

An episode key is (ha_device_id, hioc_device_id, last_confirmed_at). A prior active
pair retires once; preserve the existing record, original retired_at and reason
when that episode already exists. An inactive pair does not retire again on
every cycle. A successful later reactivation advances last_confirmed_at; a later
retirement then creates a distinct episode with that new confirmation timestamp.
Keep all prior episodes, including when a pair becomes active again. Sort history
by HA ID, HIOC ID and parsed UTC confirmation instant; sort active records by
HIOC ID then HA ID. Equivalent timestamp spellings identify the same episode.
All records for the same pair retain the same earliest first-associated instant.
Whole-item JSON Schema uniqueness is supplemented by semantic episode-key
uniqueness. Conflicting duplicate episode content fails candidate validation.

## Timestamp and cross-record invariants

updated_at is successful private-state publication time. Set last_confirmed_at
of every active pair to that successful cycle time; it means identity relationship
reconfirmation, never physical online state, entity availability or health.
first_associated_at belongs to the exact pair and stays at its earliest successful
association time. Historical last_confirmed_at never advances while inactive.
retired_at is the first successful publication retiring that episode.

Validate first_associated_at <= last_confirmed_at < retired_at <= updated_at for
history and first_associated_at <= last_confirmed_at = updated_at for active
records. Successful cycle times must advance strictly beyond prior updated_at;
a nonadvancing clock produces candidate-validation failure, not fabricated
confirmation. Reject active duplicate HIOC or HA keys, an HA ID targeting different
HIOC IDs across active/history, duplicate episode keys, rewritten existing history,
and missing required retirement records. Preserve whole prior state on failure.

JSON Schema validates shapes, bounds, enums, privacy and whole-item uniqueness.
The frozen semantic checks above are mandatory in addition; they are tested by
pure synthetic reference fixtures. No production lifecycle engine is introduced.

## Summary and count-only diagnostics

The required summary is exactly associated_devices, entity_memberships,
review_only, rejected, unmatched and historical_bindings. associated_devices is
active array length; entity_memberships is retained current entity-reference count;
historical_bindings is history-array episode count. review_only counts current
HA-device no-MAC/multiple-MAC decisions; rejected counts current rejected HA-device
decisions once per device; unmatched counts UNMATCHED_STRONG_EVIDENCE devices.
History never adds to current associated_devices or entity_memberships.

Existing outcome diagnostics remain bounded counts with a unique reason per
state. ENTITY_WITHOUT_DEVICE_IDENTITY counts the current orphan entity domain,
not rejected HA devices. PRIOR_BINDING_RETIRED counts newly added episodes in this
successful cycle; HA_DEVICE_ID_RECREATED counts successful safe rotations.
These lifecycle counts are not added again to current device outcome totals.
Failure outputs remain bounded and sanitized, never failed-state publication.
No household identifier is logged or published. Public history projection is prohibited.

## Deferred prerequisites and next task

Interactive getpass is unsuitable for unattended runtime operation. Home Assistant
Runtime Credential Provisioning remains a likely separate prerequisite to be
finalized by resumed implementation preparation; no credential interface or
provisioning is designed here. Generic StateStore.write_json alone is insufficient
for the full association locking, no-follow, ownership and durability contract.
Resumed preparation must finish that design; no writer is implemented here.

Next: PE-4 Home Assistant Association Adapter Implementation Preparation,
NOT STARTED, using both 0C and 0C.1 plus schema 1.1. PE-4 remains NOT COMPLETE,
Phase 7A ACTIVE, rollback NOT PERFORMED. Compatibility Diagnostics UX and all
other roadmap work remain preserved. No PI3/PI5/HA access, credentials,
discovery, protected rerun, MQTT publication, production state mutation, deployment,
adapter implementation or rollback occurs during this clarification.
