# PE-6 Classification & Metadata Quality — Authoritative Contract Design

Classification: CURRENT. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.

## Status, authority and evidence limits

This is PE-6.0 COMPLETE_CONTRACT_DESIGN, not implemented PE-6 runtime or phase completion.
The Master Plan owns current sequencing; this subordinate design uses existing governance conventions.
The original PE-6 architecture is c914cfc4dc39a90005bad42984396291f5b2a751:docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md#implementation-packages. Accepted baseline d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221 closes PE-5.
All technical dispositions below are PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
An implementation authorization must explicitly adopt or revise them; no design recommendation is claimed
as an inherited implemented capability. No design-blocking operator choice remains; future operational
facts remain UNKNOWN behind exact later-stage gates. No production observation or mutation occurred.

## Requirements reconciliation

- Section 1: **Permanent governing instructions** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 2: **Working model** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 3: **Access restrictions** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 4: **Establish the exact baseline** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 5: **Comprehensive existing-capability inventory** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 6: **Establish authoritative PE-6 requirements** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 7: **Classification authority and semantics** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 8: **Role suggestion contract** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 9: **Metadata quality contract** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 10: **Asset-centric compatibility** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 11: **PE-5 private handoff integration** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 12: **Complete design decisions before implementation** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 13: **Determine the complete PE-6 execution sequence** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 14: **Documentation and governance** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 15: **Validation** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 16: **Commit and independently verify** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 17: **Stop conditions** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.
- Section 18: **Required Evidence Report** — design scope reconciled; original exact instructions are preserved in the appendix; runtime/operational actions gated, never inferred.

## Existing capability inventory

Repository tests establish code behavior; historical accepted production reports are not current production facts.

### Capability 1: device identity and reconciliation

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/inventory.py:stable_device_id, merge_records, select_canonical_ip.
Tests: tests/test_inventory.py.

Existing MAC/IP/hostname fallback identity and ADR-0018 canonical comparator; PE-6 may verify existing strong-owner binding, never generate/merge/rewrite identity.

### Capability 2: private Asset foundation

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/assets.py:RECORD_KEYS, validate_store, AssetStore, AssetService.
Tests: tests/test_assets_schema.py; tests/test_assets_store.py; tests/test_assets_cli.py; tests/test_assets_orphans.py; tests/test_assets_release.py.

Schema1.0 supports friendly_name/physical_location/purpose/notes plus stable_device_id/timestamps/update_source/revision. Production acceptance is historical docs/PE2_ASSET_FOUNDATION_EVIDENCE.md, not current state proof.

### Capability 3: Asset rich management fields

Classification: PLANNED.
Authority: docs/ASSET_MODEL.md:Device and Asset; docs/PE2_ASSET_FOUNDATION_SPEC.md:Approved version1.0 fields.
Tests: tests/test_assets_schema.py:AssetSchemaTests.

Owner/category/criticality/expected availability/lifecycle/maintenance and multi-identity linking are not accepted schema1.0 fields. No Asset extension proposed here.

### Capability 4: hostname evidence

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/enrichment.py:build_hostname_envelope, validate_hostname_envelope; pi4/bin/hioc-inventory-engine.py:91-98.
Tests: tests/test_hostname_enrichment.py.

Private PE-1 envelope has source/candidate/authority/conflict/active/history semantics. Engine supplies inventory.updated as generated_at; matching time alone is not an atomic multi-file transaction.

### Capability 5: manufacturer attribution

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/manufacturer.py:validate_manufacturer_sidecar, build_manufacturer_sidecar; docs/PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md.
Tests: tests/test_manufacturer_lookup.py; tests/test_manufacturer_conflicts.py; tests/test_manufacturer_sidecar.py; tests/test_manufacturer_governance.py.

Pinned IEEE dataset/version/semantic digest; local/randomized/multicast exclusions and conflicts. Organization attribution, not device purpose/physical identity. Current injected dataset and sidecar presence UNKNOWN.

### Capability 6: Home Assistant associations

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/home_assistant_association.py:validate_state; governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json.
Tests: tests/test_pe4_ha_association_adapter.py.

Accepted private schema1.1 strong-MAC relationship producer; historical OPERATOR_SUPPLIED acceptance. No HA access or private HA collection for PE-6 design.

### Capability 7: Home Assistant public summary

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/home_assistant_public_projection.py:derive_projection, project_inventory; governance/pe4/pe4-home-assistant-public-projection.schema.json.
Tests: tests/test_pe4_ha_association_public_projection.py.

Exactly associated/association_basis/entity_count/integration_domains/has_area_candidate. No private entity IDs/names/areas. Association does not prove purpose/location/health or current HA availability.

### Capability 8: local service ownership

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/service_association.py:_owners, _owner_reason, resolve_service_associations.
Tests: tests/test_pe5_local_service_association.py.

Existing same-owner systemd/ss service relationships; strong ID check includes unique MAC and existing MAC-derived ID. Empty collection not success/absence. No new collector.

### Capability 9: configured MQTT relationships

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/configured_association.py; pi4/lib/hioc/configured_association_schemas.py; pi4/lib/hioc/configured_association_store.py:read_handoff.
Tests: tests/test_pe5_configured_association_implementation.py.

Closed source1.0/output2.0/durability1.0; opaque declared endpoints. No live Discovery/subscriber/client-topic classification authority.

### Capability 10: PE-5 private handoff

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: governance/pe5/pe5-configured-association-implementation.json#/final_closure/private_handoff.
Tests: tests/test_pe5_configured_association_implementation.py:FinalClosureTests.

Immutable accepted PE-5.9 contract and OPERATOR_SUPPLIED PE-5.6/7/8 receipts. Confirmation, input digests, revision and expiry gates remain mandatory. PE-6 does not change PE-5.

### Capability 11: known-infrastructure metadata

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/inventory.py:KNOWN_FIELDS, OPERATOR_ROLES, _clean_known_record, append_known_infrastructure.
Tests: tests/test_inventory.py.

Operator-configured role/type/vendor/model/location/area/etc. Generic merge allows more than strong-MAC identity; PE-6 confirmation proposal requires independently approved exact config bytes and unique strong-MAC binding, never public sources list alone.

### Capability 12: generic integration metadata

Classification: IMPLEMENTED_BUT_UNVERIFIED.
Authority: pi4/lib/hioc/inventory.py:integration_inventory, _select_observed_value.
Tests: tests/test_inventory.py.

Ingestion and merge are tested, but an arbitrary producer's field-specific trust, operator approval and current production values are not established. No new authority inferred.

### Capability 13: legacy derived role/type

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/inventory.py:classify_device, operator_role, inventory_class, discover_inventory.
Tests: tests/test_inventory.py:test_classification_detects_infrastructure_names; test_gateway_is_network_equipment_infrastructure; test_local_pihole_host_is_core_infrastructure; test_classification_detects_client_roles.

Existing public role can be known/integration or inferred; type/roles include route/IP/hostname/vendor/model hints. Function named operator_role does NOT establish operator confirmation. Keep all values/monitoring behavior unchanged.

### Capability 14: role_suggestion envelope

Classification: PLANNED.
Authority: docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md:field table and PE-6 row.
Tests: tests/test_pe5_configured_association_implementation.py:test_network_subprocess_and_input_authority_untouched.

No implemented PE-6 producer/schema/consumer found at baseline. New exact contract below is PROPOSED_FOR_IMPLEMENTATION_AUTHORIZATION, not running code.

### Capability 15: metadata_quality envelope

Classification: PLANNED.
Authority: docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md:Confidence model and PE-6 row.
Tests: tests/test_pe5_mapping_contract_design.py.

No implemented PE-6 quality producer found at baseline. Existing hostname quality/confidence and incident confidence_percent are unrelated scopes and cannot become a metadata score.

### Capability 16: operator_role runtime field

Classification: DESIGNED_NOT_IMPLEMENTED.
Authority: docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md:field table; pi4/lib/hioc/assets.py:RECORD_KEYS.
Tests: tests/test_assets_schema.py:test_unsupported_version_and_unknown_record_field.

Architecture reserves operator-only operator_role, but Asset schema1.0 has no such field. Proposed private derived operator_role may mirror a proved explicit known role; it is not an Asset write or a new confirmation UI.

### Capability 17: inventory validators

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/core/schemas.py:Schema.validate, INVENTORY_SCHEMA.
Tests: tests/test_core.py; tests/test_inventory.py.

Current validator checks shallow required root types, not closed per-device PE-6 semantics. Do not silently insert fields or treat a passed root validator as provenance proof.

### Capability 18: public/MQTT boundaries

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/bin/hioc-inventory-engine.py; docs/MQTT.md; docs/DATA_MODEL.md.
Tests: tests/test_inventory.py; tests/test_mqtt_dashboard_health.py.

Public inventory schema1.0/topics and existing publisher unchanged. No PE-6 public projection authorized.

### Capability 19: dashboard consumers

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: homeassistant/dashboards/living_inventory.yaml:roles/display_name; homeassistant/packages/hioc_living_inventory.yaml.
Tests: tests/test_inventory_presentation.py; tests/test_dashboard_dynamic_truth.py; tests/test_watch_device_presentation.py.

Existing dashboards consume public observed/operational fields, not private Asset or PE-6 suggestions. New UI/HA/MQTT exposure requires separate privacy/compatibility authority.

### Capability 20: private persistence/history

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/assets.py:AssetStore; pi4/lib/hioc/configured_association_store.py; docs/PE2_ASSET_IMPLEMENTATION_DESIGN.md; PE-5 corrected durability contract.
Tests: tests/test_assets_store.py; tests/test_pe5_configured_association_implementation.py:PersistenceTests.

Asset backups/revision store and PE-5 current/sidecar are distinct. No classification persistent output/history is selected by this proposal.

### Capability 21: legacy StateStore

Classification: IMPLEMENTED_AND_VALIDATED.
Authority: pi4/lib/hioc/core/state.py; docs/PE2_ASSET_IMPLEMENTATION_DESIGN.md:Existing implementation-pattern audit.
Tests: tests/test_core.py.

Existing shared state writer lacks Asset/PE-5 durability guarantees. No reuse or strengthening for a new classification store.

### Capability 22: expected availability/criticality/retention

Classification: PLANNED.
Authority: docs/ASSET_MODEL.md; docs/HIOC_MASTER_PLAN.md:Asset-centric architecture and complete PE-5 deferred work.
Tests: tests/test_assets_release.py.

PE-7 availability, later retention/archive/maintenance and PE-8/9 impact/dependencies remain separately authorized; PE-6 cannot turn quality/role into monitoring intent.

### Capability 23: pre-implementation source audits

Classification: HISTORICAL_OR_SUPERSEDED.
Authority: docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md:original enrichment source map; docs/PE2_ASSET_FOUNDATION_SPEC.md:Current operator-metadata audit.
Tests: tests/test_pe4_documentation_consistency_correction.py.

Original no-Asset/no-PE-5 statements are dated design snapshots. Actual code/current accepted closures own capability claims; historical text remains preserved.

### Capability 24: current production inputs/metadata

Classification: UNKNOWN.
Authority: No current production observation authorized by this task.
Tests: NOT_A_REPOSITORY_TEST_CLAIM.

Runtime Asset/config/hostname/manufacturer/lock presence, owners, revisions, digests and freshness remain UNKNOWN. Future operator observation is minimal and checkpoint-bounded, never inferred from these paths.

## Technical decisions

### D01 — inputs and field authority

- Existing authority: Architecture field-specific hierarchy; PE-2 closed store; PE-5.9 handoff.
- Alternatives evaluated: trust merged public role; extend Asset store; read separately validated source snapshots.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Read existing inventory plus optional Asset/PE-1/PE-3/PE-5 and explicit approved known config as separate snapshots. No implicit source promotion.
- Rationale: Merged public fields lose confirmation provenance; separate inputs preserve ownership without changing accepted models.
- Compatibility: No public inventory, Asset schema or PE-5 producer changes.
- Evidence required: Fixture each input status and exact per-field provenance; production input existence only later operator evidence.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D02 — output/API semantics

- Existing authority: Original PE-6 derived local values/rule/reasons and no operator overwrite.
- Alternatives evaluated: inline inventory fields; new persistent shared store; private stateless pure API plus explicit offline caller.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: PROPOSE pure hioc.classification.resolve_classification(inputs,evaluated_at,policy) -> closed private schema1.0 result and explicit offline caller. Names are proposed, absent at baseline.
- Rationale: Meets local explanatory capability without inventory coupling, new durability authority or recurrence requirement.
- Compatibility: No automatic consumer, daemon, cron or existing call path change.
- Evidence required: Implementation must prove no IO/clock/environment/network/subprocess in resolver and actual CLI isolation.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D03 — private/public boundary

- Existing authority: PE-2 deny-by-default Asset publication; PE-4 five-field allowlist; PE-5 private metadata.
- Alternatives evaluated: project results publicly; private results with sanitized aggregate CLI.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Private memory/API result; default CLI counts/fixed codes only. No raw Asset strings, hostname, MAC/IP, HA IDs, endpoint/topic/credential content in results/logs.
- Rationale: Private provenance may reveal relationships; no publication approval exists.
- Compatibility: MQTT/HA/dashboard/public schema bytes unchanged.
- Evidence required: Synthetic secret/redaction fixtures; all protected publisher/schema/consumer objects unchanged.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D04 — schema/versioning

- Existing authority: Existing private closed schema conventions and unchanged source schemas.
- Alternatives evaluated: extend inventory1.0; add Asset fields; independent PE-6 private1.0.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Propose closed private classification1.0 and rule_version pe6-role-v1; unknown fields/versions rejected; input schemas stay frozen. Existing role vocabulary reused but not assigned to public role.
- Rationale: Avoids breaking existing validators and confusing confirmed/derived fields.
- Compatibility: New private contract only; no runtime schema implemented now.
- Evidence required: Schema fixtures must reject authority fields, extra properties, unsupported versions and unsafe source states.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D05 — classification precedence

- Existing authority: Asset owns its four fields; known config explicit role; public role mixes inference.
- Alternatives evaluated: public role always wins; automatic reclassification; explicit source-owned confirmation plus separate suggestions.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Asset values remain untouched. Only approved original known config role with unique strong-MAC binding can populate private operator_role. Public role/type/roles never establish confirmation. No physical Asset classification field exists.
- Rationale: Source ownership is not a confidence score and cannot be inferred from aggregate sources.
- Compatibility: No rewrite of role/inventory_class/operator fields or monitoring.
- Evidence required: Test operator Unknown/clear/conflict/missing, integration spoofing and exact protected-byte identity.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D06 — role rules

- Existing authority: Architecture requires deterministic version/reasons/categorical confidence.
- Alternatives evaluated: legacy substring precedence;  source-scope capability versus physical purpose.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Propose the explicit seven-rule catalog below; active normalized hostname token rules and validated local relationship capability only. All automatic role suggestions LOW; never physical-purpose confirmation.
- Rationale: Ports/hostname/vendor/MQTT/HA alone cannot prove physical identity or purpose; weak suggestions are explainable rather than authoritative.
- Compatibility: Legacy classifier unchanged; no direct use of its output as truth.
- Evidence required: Positive/boundary/nonmatch/permutation/multiple-role fixtures and no confidence boost for correlated sources.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D07 — metadata quality

- Existing authority: Architecture enum/unknown derived completeness/conflict; not health.
- Alternatives evaluated: single opaque score;  separate dimensions plus deterministic summary enum.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Propose metadata_quality enum unknown/incomplete/documented/conflicted plus explicit quality_details dimensions. Summary describes documented descriptive knowledge, never accuracy/health/compliance.
- Rationale: Completeness, provenance, evidence reliability and operator confirmation must stay distinguishable.
- Compatibility: No numeric score or operational thresholds/incident coupling.
- Evidence required: Missing versus unavailable versus intentional N/A; weak identity and stale sources; no false all-clear.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D08 — operator confirmation/override

- Existing authority: PE-2 has no role editor; approved known-infrastructure role exists.
- Alternatives evaluated: new Asset role CLI; automatic promotion; read-only explicit known-config declaration.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: No new editor or Asset field. Explicit known role is retained separately; explicit Unknown is not absence and cannot fall through to inferred confirmation. Contradictions are surfaced with no automatic winner.
- Rationale: Avoids fabricating operator intent or extending PE-2.
- Compatibility: Existing Asset CLI/known-infrastructure editing semantics remain unchanged.
- Evidence required: Unique source/binding proof, conflicting declarations, source removal/revision, value-preservation tests.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D09 — missing/conflicting/stale inputs

- Existing authority: PE-5 safe rejection; no false absence/health; Asset existence independent of observations.
- Alternatives evaluated: fail whole inventory; reuse unverified last result; per-source availability and bounded unknown result.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Required inventory invalid -> UNAVAILABLE result, no classified devices. Optional source invalid/stale/changed -> exclude that branch and label reason; independent valid metadata remains. Never manufacture empty-success or absence.
- Rationale: Optional enrichment cannot break inventory or create a default healthy/confirmed result.
- Compatibility: No last-known-good adoption or stale persisted role.
- Evidence required: Fault fixtures for absent/unreadable/version/digest/revision/conflict/expiry and root/branch distinction.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D10 — determinism and stable IDs

- Existing authority: PE-5 stable relationship semantics; original PE-6 cycle determinism.
- Alternatives evaluated: time/random IDs; semantic version/device/role IDs.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Propose rsug_ + SHA256(canonical ASCII JSON array ['pe6-role-v1',stable_device_id,role]) without trailing newline; stable semantic ID excludes evaluation/revision/digest. Sorted rule/evidence/group lists; source changes update provenance or retract candidates.
- Rationale: Same semantic suggestion stays stable across input order and cycles, not across changed rule semantics.
- Compatibility: Never generate new device/Asset IDs or merge rotated MACs.
- Evidence required: Permutation, repeated cycles, identical duplicate, source disappearance/change and version-bump fixtures.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D11 — provenance/explainability

- Existing authority: Architecture candidate source/rule IDs; manufacturer/relationship confidence is scoped.
- Alternatives evaluated: raw values in reasons; fixed reasons plus private source/digest/evidence identifiers.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Every suggestion carries rule IDs, source/evidence IDs and correlation groups; every quality dimension has state/reason/source. Record input schema, digest, revision when meaningful, and evaluation/expiry. Never invent observed_at from config mtime.
- Rationale: Auditability without free-text leakage or overstated confidence.
- Compatibility: No re-interpretation of incident confidence_percent or OUI confidence as role certainty.
- Evidence required: Reject missing provenance, invented timestamps, duplicate amplification and unsupported source authority.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D12 — privacy/credentials

- Existing authority: Task prohibition and accepted PE-2/4/5 privacy.
- Alternatives evaluated: live queries; read accepted local artifacts only.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: No active discovery, broker/HA/API requests, credentials, DNS queries or new collectors. Future adapters read approved local paths; output and diagnostics are bounded/fixed. Raw Asset notes never parsed for suggestions.
- Rationale: Purpose/location/notes can be sensitive and are not classifier training data.
- Compatibility: No secrets/config exports or dataset redistribution.
- Evidence required: Static no-network/source inspection and synthetic credential/topic/raw-value leak fixtures.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D13 — storage/retention

- Existing authority: PE-6 local derived values do not explicitly mandate a shared store; PE-5 storage is phase-specific.
- Alternatives evaluated: new current+sidecar/cron; reuse Asset/PE-5 output; stateless on-demand result.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Select stateless private in-memory result with explicit caller; no PE-6 persistent store, journal, archive, history, LKG, cleanup or scheduler. Any future durable consumer/file is a separate accepted contract before use.
- Rationale: Avoids duplicating the established stores or inheriting unapproved durability promises.
- Compatibility: PE-2 backups and PE-5 current/sidecars untouched.
- Evidence required: Assert no write/persist paths in future pure resolver and no classification job/install initialization.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D14 — producer/consumer boundaries

- Existing authority: PE-5 read_handoff lock may create missing file; Asset shared lock can create/chmod.
- Alternatives evaluated: call arbitrary production commands; nest locks; bounded snapshot adapters plus pure resolver.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Future offline caller may only capture approved input snapshots. PE-5 Store.read_handoff(evaluated_at) keeps all gates; AssetService shared-read/lock effects must be explicitly authorized later. Do not hold different subsystem locks together; reject changed fingerprints on recheck; no retry/catch-up.
- Rationale: A reader API is not automatically filesystem-pure; coherent source snapshots require evidence.
- Compatibility: No accepted PE-5 implementation edits; no inventory engine hook.
- Evidence required: Synthetic shared/exclusive contention, missing lock, changed source and multi-input reread tests; future operator lock/metadata gate.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D15 — inventory compatibility

- Existing authority: Identity/canonical/liveness/health/incident and schema1.0 are protected; public role drives monitoring.
- Alternatives evaluated: replace role/display_name; enrich inline; parallel private result.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: All inventory fields, root schema, sources and operational classes remain byte/semantically unchanged. Only reference already accepted IDs; weak/ambiguous owner cannot gain strong relationship authority.
- Rationale: Prevents a descriptive change from altering monitoring or incidents.
- Compatibility: Existing public schema/engine/publisher/dashboard unchanged.
- Evidence required: Full inventory/monitoring/correlation/presentation regressions and exact protected field comparisons.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D16 — failure handling

- Existing authority: Accepted no-health-coupling and private safe-code patterns.
- Alternatives evaluated: raw exception details; fail-open consumer with explicit unavailable result.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Pure API returns validated result or fixed safe error; caller reports failure nonzero with no raw exception/input dump. No partial 'success' on failed required input, and no output consumer may treat unavailable as empty classification.
- Rationale: Failure must not fabricate absence or confirmation or affect base inventory.
- Compatibility: No automatic repair, mutation, deployment rollback or operational health event.
- Evidence required: Malformed root, source IO/race, serializer/caller failure and safe-code fixtures.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D17 — restart/recovery

- Existing authority: Stateless output choice; PE-5 PENDING/CONFIRMED and Asset recovery remain authoritative.
- Alternatives evaluated: adopt prior output; repair old journals; recompute from current confirmed snapshots.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: No PE-6 recovery state; restart recomputes from validated current inputs. PE-5 PENDING/missing/mismatched witness rejects affected branch and requires its existing separately approved recovery. Never recertify/write inputs here.
- Rationale: Eliminates hidden payload LKG and prevents PE-6 from taking over another writer's transactions.
- Compatibility: No changes to Asset/PE-5 recovery/backup semantics.
- Evidence required: Missing/changed/expired after restart and input journal failure fixtures, no mutation assertions.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D18 — test fixtures

- Existing authority: Original PE-6 package acceptance and user section15.
- Alternatives evaluated: happy-path only; contract+privacy+negative+cross-phase evidence.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Future implementation must satisfy the complete fixture matrix below and full native suite when source implementation changes. Current task tests design consistency, frozen Asset/PE-5 compatibility and current/historical bindings only.
- Rationale: Design tests do not prove a classifier exists or is production-ready.
- Compatibility: No production faults/collector executions for design validation.
- Evidence required: Native Windows harness, exact totals, skips, protected hashes and concise independent acceptance.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D19 — deployment/execution

- Existing authority: Accepted source/runtime separation and no production authorization now.
- Alternatives evaluated: deploy during design; auto source-to-runtime sync; separate operator source sync, disabled deployment, then bounded execution.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: Roadmap PE-6.2 source sync, PE-6.3 disabled exact artifact deployment, PE-6.4 separately authorized bounded caller execution and independent acceptance; no cron or implicit activation.
- Rationale: Source Git completion is not installed runtime or successful execution.
- Compatibility: No PI3/PI5 access, commands or observed runtime claims in this task.
- Evidence required: Later operator receipts for actual source/runtime identities, owners/modes, inputs, no protected changes; no assumptions.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

### D20 — rollback/closure

- Existing authority: Original bounded derived-only diff and protected-field preservation; PE-5 remains COMPLETE.
- Alternatives evaluated: rollback source implies runtime restore; mutate metadata on failure; stop private caller and use provenance-bound deployment rollback only if later authorized; inputs never restored/deleted by classifier.
- Disposition: PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION.
- Proposal: PE-6.5 closes only after accepted actual bounded output/schema, explanations, operator-value preservation and protected invariants. PE-7 stays separately authorized.
- Rationale: Rollback must not overwrite operator knowledge or repair unrelated historical journals.
- Compatibility: No production rollback or PE-7 action authorized here.
- Evidence required: Exact artifact/parent/subject/paths, independent GitHub retrieval and clean source; future deployment rollback receipt or explicit not-performed.
- Approval: Separate PE-6.1 authorization must explicitly adopt or revise these proposals; no runtime/production authority granted by design publication. Existing immutable boundaries need no new approval.

## Exact proposed classification and input contracts

### classification contract

- **operator_role_source**: APPROVED_ORIGINAL_KNOWN_CONFIG_WITH_UNIQUE_STRONG_MAC_BINDING_ONLY
- **public_role_is_confirmation**: false
- **asset_schema_extension**: false
- **physical_asset_classification_supported**: false
- **existing_operator_values_never_overwritten**: true
- **roles**: ["Core Infrastructure", "Network Equipment", "Server", "IoT", "Media", "Workstation", "Mobile", "Unknown"]
- **explicit_unknown_is_not_absence**: true
- **ambiguous_operator_declarations**: No selected operator_role; retain safe conflict reason. No lexical/majority automatic confirmation.
- **strong_identity**: Reuse accepted PE-5 _owner_reason eligibility: current unique ID/MAC and existing MAC-derived ID, not syntax alone. Weak/orphan Asset metadata is not deleted/rebound; ineligible identity yields unknown classification.
- **precedence**: Source ownership first; valid private Asset fields preserved independently, explicit known role separately, unconfirmed suggestions never replace either. Public role/type/roles remain compatibility data.

### input contract


{"authority": "Existing schema1.0 and strong-owner semantics; no new identity authority.", "failure": "Required invalid/unavailable/stale => UNAVAILABLE; no fabricated classified-device success.", "freshness": "PROPOSE PE-6-scoped inventory age2100 seconds, reusing accepted PE-5 private context policy explicitly as a proposal, not changing global inventory policy. Future/backward clock or at-deadline rejects.", "kind": "inventory", "required": true, "validation": "Strict new-reader admission supplements unchanged shallow root validator: typed root, unique current IDs, bounds, canonical digest and UTC updated; strong-MAC matching for eligible suggestions."}

{"authority": "Private assets.py schema1.0; exact four operator fields only.", "failure": "Absent/invalid/unreadable => explicit quality dimension missing/unknown, no initialization/repair/deletion; no copy to public fields.", "freshness": "Durable operator knowledge has no observation TTL. Snapshot digest/revision changes invalidate a result; missing current observation does not invalidate the Asset.", "kind": "assets", "required": false, "validation": "Approved snapshot via existing closed validator; exact ID/key and revision, parent/file metadata and stable recheck; private contents never echoed."}

{"authority": "Only independently approved original known-infrastructure config bytes; role enum from existing OPERATOR_ROLES.", "failure": "Unknown/unproven/ambiguous input => no confirmed role; explicit Unknown stays an explicit operator statement.", "freshness": "Configuration has content digest, not invented observation time/TTL/revision. Source removal/clear is explicit on new snapshots.", "kind": "known_operator_role", "required": false, "validation": "Exact configured snapshot identity and allowed source/ownership; normalize/validate original records; unique strong-MAC match to existing device. Never public role or aggregate sources as confirmation. Conflicting same-authority declarations retain no selected role."}

{"authority": "Validated PE-1 envelope; active selectable candidate only; its own source/candidate authority retained.", "failure": "Unpaired/stale/invalid/conflicted sources are flagged/excluded according to source semantics, never silently fresh.", "freshness": "Existing meaningful source expiry only, capped by result/inventory deadline; source mtime or last-collected time never relabeled observed_at.", "kind": "hostname", "required": false, "validation": "Closed schema, generated_at corresponds to the current inventory.updated as existing engine supplies; current unique strong ID, no historical fallback, own expires_at honored. Recheck both files/fingerprints. Timestamp equality alone is not an atomic transaction proof."}

{"authority": "PE-3 private sidecar/schema/pinned dataset provenance; organization attribution only.", "failure": "Unknown/local/randomized/multicast/conflict remains exact existing lookup disposition, no role/purpose fallback.", "freshness": "Reference attribution is not a liveness timestamp; no fake source TTL. Input digest/context change invalidates result.", "kind": "manufacturer", "required": false, "validation": "Existing closed validator; unique current strong ID and relevant MAC-prefix provenance, accepted dataset/version/semantic digest. If current binding or provenance cannot be established, mark dimension unknown; never invent inventory digest absent from schema."}

{"authority": "Existing five-field sanitized public projection only; no private HA/API/credential access.", "failure": "Omitted/invalid => unavailable relationship dimension; never negative device/health evidence.", "freshness": "Association is descriptive, not observation, HA availability or purpose proof.", "kind": "home_assistant_summary", "required": false, "validation": "Frozen public schema and current inventory association basis; no inference from private IDs/names/area or raw registries."}

{"authority": "Exact immutable PE-5.9 private handoff copied by reference and hash below.", "failure": "PENDING/missing/malformed/changed/digest/revision/clock failures reject affected input. Valid independent Asset/hostname context may still be described, never unconfirmed associations.", "freshness": "No weakening: now>=valid_until rejects; deadline min(evaluation+1200,inventory.updated+2100); no source config TTL. If used, PE-6 result cannot outlive that deadline.", "kind": "pe5_handoff", "required": false, "validation": "Use accepted Store.read_handoff(evaluated_at); output CONFIRMED and for configured VALID source CONFIRMED/domain/digest/revision; schema/current inventory/source/time/fingerprint rechecks. Root VALID is not all-branches-valid."}

### role suggestion contract

- **rules**: [{"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.hostname.media.v1", "role": "Media", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "source": "PE1_ACTIVE_HOSTNAME", "tokens": ["tv", "roku", "chromecast", "sonos", "receiver", "media"]}, {"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.hostname.mobile.v1", "role": "Mobile", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "source": "PE1_ACTIVE_HOSTNAME", "tokens": ["iphone", "ipad", "pixel", "android", "galaxy", "phone", "mobile", "tablet"]}, {"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.hostname.workstation.v1", "role": "Workstation", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "source": "PE1_ACTIVE_HOSTNAME", "tokens": ["laptop", "desktop", "workstation", "macbook", "windows"]}, {"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.hostname.iot.v1", "role": "IoT", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "source": "PE1_ACTIVE_HOSTNAME", "tokens": ["camera", "doorbell", "printer", "thermostat", "sensor", "plug", "bulb", "matter", "zigbee", "zwave"]}, {"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.hostname.server.v1", "role": "Server", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "source": "PE1_ACTIVE_HOSTNAME", "tokens": ["server", "nas", "proxmox", "docker", "ubuntu", "debian", "homeassistant", "haos"]}, {"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.hostname.network.v1", "role": "Network Equipment", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "source": "PE1_ACTIVE_HOSTNAME", "tokens": ["orbi", "satellite", "mesh", "switch"]}, {"authority": "UNCONFIRMED_SUGGESTION", "confidence": "low", "correlation_policy": "Same PE-1 candidate family or PE-5 underlying service tuple is one group; repeated/correlated sources never boost confidence.", "id": "pe6.local.service.v1", "role": "Core Infrastructure", "scope": "technical_role_hypothesis_not_physical_asset_purpose", "service_types": ["mqtt", "dns", "dhcp", "ups", "scheduler"], "source": "PE5_CONFIRMED_LOCAL_RELATIONSHIP"}]
- **confidence_categories**: ["authoritative", "high", "medium", "low", "unknown"]
- **automatic_confidence**: low
- **numeric_confidence**: false
- **tokenization**: PROPOSE ASCII lowercase tokenization of validated normalized PE-1 hostname using maximal [a-z0-9]+ words; exact token membership only, no substring/regex/ML/network lookup. Non-ASCII/punycode uncertainty cannot create an unsupported token rule.
- **excluded_sources**: ["manufacturer_alone", "port_alone", "MQTT_edge_alone", "HA_association_or_domain_alone", "IP_or_subnet", "raw_Asset_notes_or_purpose", "public_role_as_operator_proof", "historical_or_expired_hostname"]
- **semantic_identity**: rsug_ + SHA256(canonical ASCII JSON array ['pe6-role-v1',stable_device_id,role] without trailing newline); excludes evaluation, input revision/digest and number of correlated sources.
- **evidence_identity**: Each evidence_id is SHA256 of canonical ASCII JSON [stable_device_id,source_kind,input_snapshot_sha256,original_candidate_or_relationship_id], without trailing newline; it is provenance, not a device identity. Correlation group is SHA256 of [pe6-group-v1,stable_device_id,hostname-or-local_service] in the same canonical encoding. All hostname sources collapse to one coarse family and all local services to one family per device. Groups do not assert independence and never boost LOW confidence.
- **aggregation**: One candidate per device/role with sorted distinct rule/evidence IDs and correlation groups. LOW remains LOW even with multiple correlated or independent weak inputs; no numerical voting. Multiple distinct roles remain unconfirmed alternatives, no automatic winner.
- **missing**: [] with explicit reason/state; no available suggestions does not mean successful collection, no physical role or healthy device.

### metadata quality contract

- **summary_values**: ["unknown", "incomplete", "documented", "conflicted"]
- **precedence**: ["conflicted", "unknown", "incomplete", "documented"]
- **definitions**: {"conflicted": "Usable accepted source explicitly reports competing same-field descriptive metadata (for example PE-1 current hostname conflict), or proved contradictory explicit role declarations. Preserve operator-owned values and reasons; no health impact.", "documented": "Unique strong context and valid exact-ID Asset record with all three friendly_name/physical_location/purpose non-null, with no assessed conflict/unknown condition above. This is documentation completeness, not truth, health, confirmed physical class or all-source success.", "incomplete": "Identity/context assessable but valid Asset store/record absent or one of friendly_name/physical_location/purpose null; exact missing field identifiers only, no score.", "unknown": "No eligible unique strong identity or Asset snapshot missing validity/provenance; inability to assess is not zero completeness. Explicitly absent valid input may be known missing instead."}
- **dimensions**: [{"definition": "Existing identity eligibility/provenance only; never creates/merges identity or estimates health.", "name": "identity", "states": ["strong", "weak", "ambiguous", "unknown"]}, {"definition": "Known presence of friendly_name/physical_location/purpose in valid exact-ID Asset record; notes optional/private and never scored. No raw values in report.", "name": "asset_documentation", "states": ["documented", "incomplete", "missing", "unknown"]}, {"definition": "Existing PE-3 source-scoped disposition, not physical identity/purpose certainty.", "name": "manufacturer_attribution", "states": ["matched", "unknown", "excluded", "conflicted", "unverified"]}, {"definition": "Explicit approved original config role only; no generic public-role confirmation.", "name": "operator_role_confirmation", "states": ["declared", "explicit_unknown", "missing", "conflicted", "unverified"]}, {"definition": "PE-2.1 has no classification field/editor; not missing data or a silently authorized extension.", "name": "physical_asset_classification", "states": ["not_supported_current_schema"]}, {"definition": "Unconfirmed hypotheses; multiple possible roles do not automatically mean an operator metadata contradiction.", "name": "role_suggestions", "states": ["single", "multiple", "none", "unavailable"]}, {"definition": "Accepted HA/PE-5 descriptive provenance only; no health/availability inference.", "name": "relationship_evidence", "states": ["available", "partial", "unavailable", "unverified"]}, {"definition": "Per-source schema/binding/expiry/recheck outcomes; source confirmation distinct from role confidence.", "name": "provenance_and_freshness", "states": ["verified", "partial", "conflicted", "unknown"]}]
- **not_applicable_policy**: Only explicitly declared schema/policy exemption can be not applicable; unsupported physical Asset class is separately not_supported_current_schema. Missing values never silently become N/A.
- **numerical_score**: false
- **notes_required**: false
- **quality_is_health**: false
- **quality_is_availability**: false

### output semantics

- **status**: PROPOSED_NOT_IMPLEMENTED
- **private_only**: true
- **storage**: STATELESS_IN_MEMORY_ONLY
- **persistent_store_required**: false
- **recurring_execution_required**: false
- **inventory_hook**: false
- **public_projection_authorized**: false
- **unavailable**: Required inventory invalid => state UNAVAILABLE, valid_until null, devices empty and explicit input failure; never VALID-empty fallback. Empty valid inventory is allowed with corresponding valid input proof.
- **partial**: Optional rejected input => PARTIAL and source reason; independent valid sources remain usable within their authority.
- **deadline**: PROPOSE PE-6 inventory deadline inventory.updated+2100; if accepted PE-5 evidence used, cap by its existing valid_until; cap further by any genuinely supplied earlier source expiry. Reject current time>=deadline, future/backward clock or changed input fingerprints. Asset/configuration validity itself has no observation TTL.
- **cross_fields**: Future semantic validator must require exact counts, sorted unique device/candidate/rule/evidence arrays, allowed dimension-specific states, valid IDs/provenance, operator source proof, non-amplified categorical confidence, matching input fingerprints and original-source schemas. JSON shape alone is insufficient.
- **maximum_devices**: 4096
- **maximum_input_bytes_per_source**: 16777216
- **maximum_output_bytes**: 16777216
- **bounds_rationale**: Proposed new-reader admission bounds reuse existing PE-5 private-envelope limits; they never invalidate or mutate an existing larger Asset store. Over-limit input yields explicit unavailable branch/result.
- **private_api**: PROPOSE hioc.classification.resolve_classification(inputs,evaluated_at,policy) -> dict; pure, no IO/clock/env/random/subprocess/network. Caller injects time and validated immutable snapshots.
- **consumer_api**: PROPOSE hioc.classification.validate_classification_result(result,current_inputs,evaluated_at) -> None or fixed safe error. Every use revalidates closed/semantic shape, current input digests/source authority and a newly caller-supplied current time against deadline; elapsed processing never refreshes result time. No stored result is self-authenticating. OPERATOR_DECLARED/EXPLICIT_UNKNOWN require operator_role_evidence matching approved known-config proof; all other states must not fabricate it.
- **proposed_caller**: PROPOSE pi4/bin/hioc-classify-metadata.py; explicitly invoked, default sanitized aggregate summary; private result never exposed by default or written to existing stores.
- **overflow**: Any declared source/device/candidate/provenance/output admission-bound overflow yields explicit LIMIT_EXCEEDED/UNAVAILABLE result, no truncation or silently dropped evidence; existing source stores remain unchanged.
- **no_output_file**: true
- **no_last_known_good**: true
- **no_new_scheduler**: true
- **no_new_producer_execution**: true

### private handoff

- **accepted_pe5**: {"authority": "72e878f9c0c8f5d3fe6357979e045943f3cf9d34:governance/pe5/pe5-atomic-durability-contract-correction.json", "bounds": {"mapping_rows": 4096, "metadata_bytes": 8192, "output_bytes": 16777216, "source_bytes": 262144}, "cadence": "2,17,32,47 * * * *; independent composer every900 seconds, no catch-up/retry", "changes_bound": "added/removed relationship-ID arrays at most64 each; exact total counts and truncation flag, no invented removal from unavailable/noncomparable prior.", "changes_fields": ["added", "added_count", "baseline", "removed", "removed_count", "truncated"], "command": "/usr/bin/python3 /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py", "configured_fields": ["associations", "candidate_count", "error_code", "rejections", "revision", "source_id", "source_sha256", "state"], "configured_states": ["VALID", "UNAVAILABLE"], "configured_valid_requires_confirmed_source": true, "consumer": "Future PE-6 private relationship reader only; no current PE-6 implementation or runtime authorization.", "durability": "PENDING barrier -> exclusive temporary write/file fsync -> one primary replace -> parent fsync -> CONFIRMED sidecar/file/parent barriers. Pre-replace failure preserves prior; post-replace parent failure is INDETERMINATE/WRITE_FAILED, not rollback success.", "freshness": "Inventory age <=2100 seconds with accepted clock rules; output valid_until=min(evaluated_at+1200,inventory.updated+2100). Reject at now>=valid_until and on future/backward clock or changed consumed inventory/source identity.", "identifiers": "Opaque endpoint me_[0-9a-f]{32}; row map_[0-9a-f]{32}; existing strong dev_[0-9a-f]{16}; optional existing same-owner service.", "inventory": "state/inventory/inventory.json", "local_state_field_defined": false, "lock": "state/enrichment/service_associations/.lock", "mapping_fields": ["mapping_id", "endpoint_id", "device_id", "service_id"], "metadata_descriptor_contract": "Closed schema1.0: dur_[0-9a-f]{32} transaction_id; PENDING requires candidate descriptor and nullable prior confirmed; CONFIRMED requires candidate=null and confirmed descriptor. Descriptors contain only sha256 (64 lowercase hex) and source_revision. Source revision is integer1..9007199254740991; output source_revision may be null for no configured revision. Exact current bytes/domain/revision must match; filenames alone are not confirmation.", "metadata_domains": ["CONFIGURED_MAPPING_SOURCE", "GENERATED_RELATIONSHIP_OUTPUT"], "metadata_fields": ["candidate", "confirmed", "domain", "schema_version", "state", "transaction_id"], "missing_and_errors": "Absent/invalid source may preserve independent local output only with confirmed current output and valid current inputs/schema/time; local null is unavailable, not empty/success. Explicit empty source is known-empty; reject conflicting/duplicate or unknown-owner configured rows per contract.", "output": "state/enrichment/service_associations/current.json", "output_fields": ["changes", "configured", "evaluated_at", "inventory", "local", "schema_version", "state", "valid_until"], "output_metadata": "state/enrichment/service_associations/current.durability.json", "pe6_responsibility": "Separately authorized explainable classification/role_suggestion/metadata_quality design and validation; protect operator_role, provenance/privacy/time/rejection and reader-lock lifecycle; no automatic promotion of relationships.", "permissions": "Private parents 0700; regular nonlink single-link files 0600; owner jazofv1, accepted operator UID/GID1000/1000. Future consumer must enforce safety; no permission change here.", "private_only": true, "producer": "Approved offline installer writes source; standalone recurring composer writes output; never inventory engine or caller hook.", "prohibited_authority": ["identity", "canonical_ip", "observation", "liveness", "health", "asset_classification", "operator_role"], "provenance": "source_kind configured_mqtt, rule_id declared_endpoint_device_v1; source_id/revision/digest/mapping_id remain private. Local schema unchanged.", "public_boundary": "No raw private source/output/endpoint/topic/credential exposure, public schema change, publication/subscription or inference of MQTT broker health.", "reader_api": "hioc.configured_association_store.Store.read_handoff(evaluated_at)", "reader_lock_may_create_file": true, "reader_lock_note": "Store.lock() uses nonblocking exclusive flock and may create missing .lock in approved private parent. Existing API is not a filesystem-pure read; future PE-6 must explicitly govern reader/lock lifecycle. Do not call it in PE-5.9.", "recovery": "Only separately approved recertification of exact recorded candidate/prior, fsync without primary replacement or time refresh; unmatched/corrupt bytes stop. Fresh producer recomputation is separate approved action.", "relationship_fields": ["device_id", "direction", "endpoint_id", "mapping_id", "relationship_id", "rule_id", "service_id", "source_id", "source_kind", "source_revision", "source_sha256"], "relationship_identity": "mqra_ + SHA256(ASCII canonical JSON array ['configured_mqtt_v1',source_id,endpoint_id,device_id,service_id,'endpoint_to_device']); excludes revision, mapping_id and evaluation.", "required_output_confirmation": "CONFIRMED matching current output digest/domain/revision, closed schema, stable read fingerprint; reject PENDING/missing/malformed/mismatched sidecar.", "retention": "One current primary per domain and bounded sidecar descriptors; no archive/application-payload LKG replay. Stale crash temporaries never adopted; cleanup not authorized.", "revision": "Integer 1..9007199254740991, never bool; approved content changes increment revision; rollback or equal revision with changed content rejected; PENDING recovery floors enforced. No source TTL/observed_at/mtime authority.", "root": "/home/jazofv1/hioc", "schema_authority": {"input_schema": "c4ca34ae123617769d25a694d55f50473d7f69670974e6cfae2a9607e9bbe6c4", "metadata_schema": "18c041c4d2dafb3d7420260a5fe4fc8edf8aee6759253a9f4ad8e8683a75972c", "output_schema": "c2e33c2cbaa1c26d73f153a5dcd4be224c96b682e793a6b751f3d63d9ed6bba6"}, "source": "config/enrichment/mqtt_mappings.json", "source_confirmation": "For configured VALID require CONFIRMED current source digest/revision and final source/output rechecks under lock. Root VALID alone does not establish all branches valid.", "source_fields": ["schema_version", "source_id", "revision", "mappings"], "source_id": "operator_mqtt_v1 (exact schema constant)", "source_metadata": "config/enrichment/mqtt_mappings.durability.json", "versions": {"durability": "1.0", "local": "1.0", "output": "2.0", "source": "1.0"}}
- **pe5_record_sha256**: 56fb0f59c4be7ae8fc8d248c6e6e0f173e314765e465454ed9fe449ace45843d
- **pe5_schema_sha256**: 8cce5576dd47be3e3d194ba90cadd102ffc0053392d840886d269e489d3d9134
- **reader_side_effects**: Future caller must explicitly authorize existing PE-5 lock lifecycle (may create .lock) and Asset shared lock creation/chmod within approved exact paths; do not call either API on production now. Do not nest locks across subsystems; capture/release/recheck input identity, reject races without retry. No producer, recovery, scheduler or source/output replacement.
- **current_production_state**: UNKNOWN; no current lock/input/store/source/runtime observation made or requested

## Proposed private schema and semantic validation

The exact closed JSON shape below is declarative design, NOT implemented runtime validation.
Cross-field, provenance, clock, counts, sorted uniqueness, source ownership, dimension-specific state
and safe-admission rules above are mandatory in PE-6.1. Shape validation alone never authorizes use.

~~~json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PROPOSED private PE-6 classification envelope1.0; not implemented",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "devices",
    "evaluated_at",
    "inputs",
    "rule_version",
    "schema_version",
    "state",
    "summary",
    "valid_until"
  ],
  "properties": {
    "schema_version": {
      "const": "1.0"
    },
    "rule_version": {
      "const": "pe6-role-v1"
    },
    "state": {
      "enum": [
        "VALID",
        "PARTIAL",
        "UNAVAILABLE"
      ]
    },
    "evaluated_at": {
      "type": "string",
      "format": "date-time",
      "maxLength": 32,
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$"
    },
    "valid_until": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time",
          "maxLength": 32,
          "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$"
        },
        {
          "type": "null"
        }
      ]
    },
    "inputs": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "generated_at",
          "kind",
          "reason_code",
          "revision",
          "sha256",
          "state"
        ],
        "properties": {
          "kind": {
            "enum": [
              "inventory",
              "assets",
              "known_operator_role",
              "hostname",
              "manufacturer",
              "home_assistant_summary",
              "pe5_handoff"
            ]
          },
          "state": {
            "enum": [
              "VALID",
              "ABSENT",
              "UNAVAILABLE",
              "INVALID",
              "STALE",
              "CONFLICTED"
            ]
          },
          "sha256": {
            "anyOf": [
              {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$"
              },
              {
                "type": "null"
              }
            ]
          },
          "revision": {
            "anyOf": [
              {
                "type": "integer",
                "minimum": 1,
                "maximum": 9007199254740991
              },
              {
                "type": "null"
              }
            ]
          },
          "generated_at": {
            "anyOf": [
              {
                "type": "string",
                "format": "date-time",
                "maxLength": 32,
                "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$"
              },
              {
                "type": "null"
              }
            ]
          },
          "reason_code": {
            "enum": [
              "VALIDATED",
              "ABSENT",
              "UNAVAILABLE",
              "INVALID",
              "STALE",
              "CHANGED",
              "CONFLICTED",
              "NOT_SUPPORTED",
              "INCOMPLETE",
              "INSUFFICIENT_EVIDENCE",
              "LIMIT_EXCEEDED"
            ]
          }
        }
      },
      "maxItems": 7
    },
    "devices": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "classification_status",
          "identity_status",
          "metadata_quality",
          "operator_role",
          "operator_role_evidence",
          "quality_details",
          "reason_codes",
          "role_suggestion",
          "stable_device_id"
        ],
        "properties": {
          "stable_device_id": {
            "type": "string",
            "pattern": "^dev_[0-9a-f]{16}$"
          },
          "identity_status": {
            "enum": [
              "strong",
              "weak",
              "ambiguous",
              "unknown"
            ]
          },
          "operator_role": {
            "anyOf": [
              {
                "enum": [
                  "Core Infrastructure",
                  "Network Equipment",
                  "Server",
                  "IoT",
                  "Media",
                  "Workstation",
                  "Mobile",
                  "Unknown"
                ]
              },
              {
                "type": "null"
              }
            ]
          },
          "operator_role_evidence": {
            "anyOf": [
              {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$"
              },
              {
                "type": "null"
              }
            ]
          },
          "classification_status": {
            "enum": [
              "OPERATOR_DECLARED",
              "EXPLICIT_UNKNOWN",
              "UNCONFIRMED",
              "AMBIGUOUS",
              "UNKNOWN"
            ]
          },
          "role_suggestion": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": [
                "confidence",
                "correlation_groups",
                "evidence_ids",
                "role",
                "rule_ids",
                "suggestion_id"
              ],
              "properties": {
                "suggestion_id": {
                  "type": "string",
                  "pattern": "^rsug_[0-9a-f]{64}$"
                },
                "role": {
                  "enum": [
                    "Core Infrastructure",
                    "Network Equipment",
                    "Server",
                    "IoT",
                    "Media",
                    "Workstation",
                    "Mobile"
                  ]
                },
                "rule_ids": {
                  "type": "array",
                  "items": {
                    "enum": [
                      "pe6.hostname.media.v1",
                      "pe6.hostname.mobile.v1",
                      "pe6.hostname.workstation.v1",
                      "pe6.hostname.iot.v1",
                      "pe6.hostname.server.v1",
                      "pe6.hostname.network.v1",
                      "pe6.local.service.v1"
                    ]
                  },
                  "maxItems": 7
                },
                "confidence": {
                  "const": "low"
                },
                "evidence_ids": {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "pattern": "^[0-9a-f]{64}$"
                  },
                  "maxItems": 64
                },
                "correlation_groups": {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "pattern": "^[0-9a-f]{64}$"
                  },
                  "maxItems": 64
                }
              }
            },
            "maxItems": 7
          },
          "metadata_quality": {
            "enum": [
              "unknown",
              "incomplete",
              "documented",
              "conflicted"
            ]
          },
          "quality_details": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": [
                "name",
                "reason_code",
                "source_kind",
                "state"
              ],
              "properties": {
                "name": {
                  "enum": [
                    "identity",
                    "asset_documentation",
                    "manufacturer_attribution",
                    "operator_role_confirmation",
                    "physical_asset_classification",
                    "role_suggestions",
                    "relationship_evidence",
                    "provenance_and_freshness"
                  ]
                },
                "state": {
                  "enum": [
                    "ambiguous",
                    "available",
                    "conflicted",
                    "declared",
                    "documented",
                    "excluded",
                    "explicit_unknown",
                    "incomplete",
                    "matched",
                    "missing",
                    "multiple",
                    "none",
                    "not_supported_current_schema",
                    "partial",
                    "single",
                    "strong",
                    "unavailable",
                    "unknown",
                    "unverified",
                    "verified",
                    "weak"
                  ]
                },
                "source_kind": {
                  "enum": [
                    "inventory",
                    "assets",
                    "known_operator_role",
                    "hostname",
                    "manufacturer",
                    "home_assistant_summary",
                    "pe5_handoff"
                  ]
                },
                "reason_code": {
                  "enum": [
                    "VALIDATED",
                    "ABSENT",
                    "UNAVAILABLE",
                    "INVALID",
                    "STALE",
                    "CHANGED",
                    "CONFLICTED",
                    "NOT_SUPPORTED",
                    "INCOMPLETE",
                    "INSUFFICIENT_EVIDENCE",
                    "LIMIT_EXCEEDED"
                  ]
                }
              }
            },
            "maxItems": 8
          },
          "reason_codes": {
            "type": "array",
            "items": {
              "enum": [
                "VALIDATED",
                "ABSENT",
                "UNAVAILABLE",
                "INVALID",
                "STALE",
                "CHANGED",
                "CONFLICTED",
                "NOT_SUPPORTED",
                "INCOMPLETE",
                "INSUFFICIENT_EVIDENCE",
                "LIMIT_EXCEEDED"
              ]
            },
            "maxItems": 16
          }
        }
      },
      "maxItems": 4096
    },
    "summary": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "conflicted_count",
        "device_count",
        "suggestion_count",
        "unavailable_source_count"
      ],
      "properties": {
        "device_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 4096
        },
        "suggestion_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 28672
        },
        "conflicted_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 4096
        },
        "unavailable_source_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 7
        }
      }
    }
  }
}
~~~

## Complete proposed execution roadmap

Six checkpoints preserve actual risk distinctions: contract; implementation; source-only sync; disabled runtime installation;
bounded execution plus concise independent acceptance; final governance closure. Independent acceptance is combined
with execution review, not made another production action. No recurring-execution stage is manufactured because
this proposal requires no classification persistence or schedule. All checkpoints after this design are NOT AUTHORIZED.

### PE-6.0 — Authoritative contract design and execution roadmap

- **objective**: Authoritative contract design and execution roadmap
- **scope**: Repository investigation and proposed contracts only; this authorized task.
- **dependencies**: ["PE-5.9"]
- **inputs**: ["Exact accepted predecessor contract/commit and applicable source/runtime evidence"]
- **outputs**: ["Sanitized exact Evidence Report, accepted artifact/decision identities and explicit next gate"]
- **access**: WINDOWS_REPOSITORY_ONLY
- **allowed_changes**: Repository investigation and proposed contracts only; this authorized task.
- **tests**: Native focused/current bindings/Asset/PE-5/privacy/cross-phase regression; full native suite if runtime source changes
- **acceptance**: No unknown prerequisite, no unauthorized write/authority/privacy change, exact observed validation and concise independent acceptance
- **operator_action**: NONE
- **stop_conditions**: ["Missing authority or operator adoption", "Input/identity/protected/privacy mismatch", "Failed validation", "Production necessary without separate authority", "Unresolved material decision"]
- **successor**: PE-6.1
- **status**: COMPLETE_CONTRACT_DESIGN

### PE-6.1 — Private classification implementation and comprehensive repository validation

- **objective**: Private classification implementation and comprehensive repository validation
- **scope**: Separate authorization explicitly adopts/revises all proposals before product source changes; full native suite for source implementation.
- **dependencies**: ["PE-6.0"]
- **inputs**: ["Exact accepted predecessor contract/commit and applicable source/runtime evidence"]
- **outputs**: ["Sanitized exact Evidence Report, accepted artifact/decision identities and explicit next gate"]
- **access**: WINDOWS_REPOSITORY_ONLY
- **allowed_changes**: Separate authorization explicitly adopts/revises all proposals before product source changes; full native suite for source implementation.
- **tests**: Native focused/current bindings/Asset/PE-5/privacy/cross-phase regression; full native suite if runtime source changes
- **acceptance**: No unknown prerequisite, no unauthorized write/authority/privacy change, exact observed validation and concise independent acceptance
- **operator_action**: NONE
- **stop_conditions**: ["Missing authority or operator adoption", "Input/identity/protected/privacy mismatch", "Failed validation", "Production necessary without separate authority", "Unresolved material decision"]
- **successor**: PE-6.2
- **status**: PLANNED_ONLY_NOT_AUTHORIZED

### PE-6.2 — PI3 release-source synchronization

- **objective**: PI3 release-source synchronization
- **scope**: Operator-only source Git action, exact fast-forward and clean source receipt; no runtime deployment/execution.
- **dependencies**: ["PE-6.1"]
- **inputs**: ["Exact accepted predecessor contract/commit and applicable source/runtime evidence"]
- **outputs**: ["Sanitized exact Evidence Report, accepted artifact/decision identities and explicit next gate"]
- **access**: OPERATOR_ONLY_SEPARATE_AUTHORIZATION; CODEX_NO_PRODUCTION
- **allowed_changes**: Operator-only source Git action, exact fast-forward and clean source receipt; no runtime deployment/execution.
- **tests**: Exact artifact/provenance/protected-field checks and bounded synthetic tests applicable to this risk boundary
- **acceptance**: No unknown prerequisite, no unauthorized write/authority/privacy change, exact observed validation and concise independent acceptance
- **operator_action**: Operator-only source Git action, exact fast-forward and clean source receipt; no runtime deployment/execution.
- **stop_conditions**: ["Missing authority or operator adoption", "Input/identity/protected/privacy mismatch", "Failed validation", "Production necessary without separate authority", "Unresolved material decision"]
- **successor**: PE-6.3
- **status**: PLANNED_ONLY_NOT_AUTHORIZED

### PE-6.3 — Disabled exact runtime deployment

- **objective**: Disabled exact runtime deployment
- **scope**: Operator-only approved artifact/metadata installation and provenance-bound backup; no caller execution/cron/initialization.
- **dependencies**: ["PE-6.2"]
- **inputs**: ["Exact accepted predecessor contract/commit and applicable source/runtime evidence"]
- **outputs**: ["Sanitized exact Evidence Report, accepted artifact/decision identities and explicit next gate"]
- **access**: OPERATOR_ONLY_SEPARATE_AUTHORIZATION; CODEX_NO_PRODUCTION
- **allowed_changes**: Operator-only approved artifact/metadata installation and provenance-bound backup; no caller execution/cron/initialization.
- **tests**: Exact artifact/provenance/protected-field checks and bounded synthetic tests applicable to this risk boundary
- **acceptance**: No unknown prerequisite, no unauthorized write/authority/privacy change, exact observed validation and concise independent acceptance
- **operator_action**: Operator-only approved artifact/metadata installation and provenance-bound backup; no caller execution/cron/initialization.
- **stop_conditions**: ["Missing authority or operator adoption", "Input/identity/protected/privacy mismatch", "Failed validation", "Production necessary without separate authority", "Unresolved material decision"]
- **successor**: PE-6.4
- **status**: PLANNED_ONLY_NOT_AUTHORIZED

### PE-6.4 — Bounded execution and concise independent production acceptance

- **objective**: Bounded execution and concise independent production acceptance
- **scope**: Separately authorized operator-only offline caller once on approved input snapshots; sanitized schema/count/hash/explanation/protected-invariant receipt, then repository independent acceptance. No automated recurring activation.
- **dependencies**: ["PE-6.3"]
- **inputs**: ["Exact accepted predecessor contract/commit and applicable source/runtime evidence"]
- **outputs**: ["Sanitized exact Evidence Report, accepted artifact/decision identities and explicit next gate"]
- **access**: OPERATOR_ONLY_SEPARATE_AUTHORIZATION; CODEX_NO_PRODUCTION
- **allowed_changes**: Separately authorized operator-only offline caller once on approved input snapshots; sanitized schema/count/hash/explanation/protected-invariant receipt, then repository independent acceptance. No automated recurring activation.
- **tests**: Exact artifact/provenance/protected-field checks and bounded synthetic tests applicable to this risk boundary
- **acceptance**: No unknown prerequisite, no unauthorized write/authority/privacy change, exact observed validation and concise independent acceptance
- **operator_action**: Separately authorized operator-only offline caller once on approved input snapshots; sanitized schema/count/hash/explanation/protected-invariant receipt, then repository independent acceptance. No automated recurring activation.
- **stop_conditions**: ["Missing authority or operator adoption", "Input/identity/protected/privacy mismatch", "Failed validation", "Production necessary without separate authority", "Unresolved material decision"]
- **successor**: PE-6.5
- **status**: PLANNED_ONLY_NOT_AUTHORIZED

### PE-6.5 — Final PE-6 governance closure and PE-7 handoff

- **objective**: Final PE-6 governance closure and PE-7 handoff
- **scope**: Repository-only closure after all actual required evidence passes; no repeated production action. PE-7 remains separate authorization.
- **dependencies**: ["PE-6.4"]
- **inputs**: ["Exact accepted predecessor contract/commit and applicable source/runtime evidence"]
- **outputs**: ["Sanitized exact Evidence Report, accepted artifact/decision identities and explicit next gate"]
- **access**: WINDOWS_REPOSITORY_ONLY
- **allowed_changes**: Repository-only closure after all actual required evidence passes; no repeated production action. PE-7 remains separate authorization.
- **tests**: Exact artifact/provenance/protected-field checks and bounded synthetic tests applicable to this risk boundary
- **acceptance**: No unknown prerequisite, no unauthorized write/authority/privacy change, exact observed validation and concise independent acceptance
- **operator_action**: NONE
- **stop_conditions**: ["Missing authority or operator adoption", "Input/identity/protected/privacy mismatch", "Failed validation", "Production necessary without separate authority", "Unresolved material decision"]
- **successor**: PE-7
- **status**: PLANNED_ONLY_NOT_AUTHORIZED

## Required implementation fixture matrix

Current schema/design tests do not prove these runtime behaviors implemented.
PE-6.1 must implement and pass every applicable case before deployment preparation.

1. exact inventory/Asset/PE1/PE3/HA/PE5 schemas and unknown version/field rejection.
2. unique strong MAC owner, weak ID, duplicate ID/MAC, owner mismatch and no identity merge.
3. empty inventory versus invalid inventory, missing Asset store/record, Asset orphan and invalid schema.
4. each hostname token positive/nonmatch/boundary/case and Unicode normalization rejection.
5. active versus historical/expired hostname; generated_at/current inventory binding and source changed.
6. single/multiple suggestion roles, deterministic ordering and no automatic winner.
7. same source through hostname/HA/MQTT views deduplicated, no correlated confidence boost.
8. operator known role source proof, explicit Unknown, absent and source removal.
9. operator Asset values preserved byte-for-byte; public role never confirmation; integration spoofing rejected.
10. conflicting explicit declarations, PE1 conflict flag and metadata conflict reasons without health effect.
11. manufacturer unknown/local/randomized/conflict/pinned dataset proof; no OUI-to-purpose inference.
12. HA five-field summary allowlist only; no entity/domain/area-to-purpose/location inference.
13. opaque configured MQTT association by itself emits no role suggestion.
14. PE5 local ownership rule accepted only through exact confirmed current handoff.
15. missing/PENDING/malformed/wrong-domain/digest/revision/output/source confirmation safe rejection.
16. inventory2100 and PE5 min1200 cap; exact expiry boundary/future/backward clock reject.
17. metadata completeness versus provenance versus confirmation states, missing versus unavailable.
18. not_applicable only by explicit declared field policy; unsupported Asset fields not empty data.
19. private raw notes/location/name/MAC/IP/hostname/topic/credential not echoed in role reasons/default CLI.
20. deterministic semantic IDs across cycles/permutations, source revision/digest changes and retraction.
21. immutable input dictionaries; no inventory/Asset/PE5/publisher/scheduler writes.
22. no resolver IO/clock/environment/subprocess/network; fixed error codes and unavailable consumer.
23. shared Asset lock and PE5 lock lifecycle side effects explicitly bounded; no nested locks.
24. source/read fingerprint race; no unapproved retry/adoption/transaction recovery.
25. restart from confirmed inputs, stale prior result not LKG, no cleanup/history/store creation.
26. maximum4096-device/mapping and16MiB admission bounds, bounded candidate/provenance lists.
27. legacy role/class/monitoring/health/incident/public inventory byte and semantic compatibility.
28. cross-phase historical authority frozen while current documentation bindings follow PE6.
29. later native disabled deployment evidence separated from bounded production execution.
30. bounded derived-only comparison and independent acceptance before final PE6/PE7 handoff.

## Operator decisions, UNKNOWN facts and deferred capabilities

{
  "design_blockers": [],
  "proposal_adoption": "Separate PE-6.1 implementation authorization must adopt/revise the proposed rules, metadata semantics, private API/stateless execution and PE-6-scoped2100 freshness policy.",
  "operational_facts": [
    {
      "fact": "Actual PI3 source/runtime baseline and installed artifact metadata",
      "status": "UNKNOWN_NOT_OBSERVED",
      "resolved_before": "PE-6.2/PE-6.3 operator gates"
    },
    {
      "fact": "Actual optional input presence/owners/modes/digests/revisions and existing lock lifecycle",
      "status": "UNKNOWN_NOT_OBSERVED",
      "resolved_before": "PE-6.3/PE-6.4 minimal bounded operator gates"
    },
    {
      "fact": "Actual bounded classification result/explanations and protected before/after invariants",
      "status": "UNKNOWN_NOT_OBSERVED",
      "resolved_before": "PE-6.4"
    }
  ],
  "later_choices": "Physical Asset category/owner/criticality/availability/lifecycle/multi-ID linkage and public UI/projection require their separately authorized phase/contract, not silent PE-6 implementation."
}

The proposed PE-6 scope does not implement Asset owner/category/criticality/availability/lifecycle/linking,
PE-7 monitoring, PE-8 functional impact, PE-9 technical dependency inference, PE-10 surveillance,
retention/archive, Active Discovery, or public/UI projection. Existing PE-5 deferred_work remains unchanged.
Operator data outlives stale observations; no suggestion or quality category is permission to archive, merge,
monitor, create incidents or overwrite Asset knowledge. Physical Asset confirmation needs a future accepted model.

## Native Windows validation and publication evidence

Bundled interpreter: C:/Users/JorgeAzofeifaCastill/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B - with stdin unittest harness, Windows repository root working directory.
PYTHONUTF8=1; PYTHONDONTWRITEBYTECODE=1; HIOC_TEST_SHELL removed; sys.path[:0]=['tests','pi4/lib'].
Shell-free PATH contains only Windows/System32, Windows root, WindowsPowerShell/v1.0, Git/cmd and the interpreter parent.
Baseline selections: discover('tests',pattern='test_assets*.py'); loadTestsFromName('test_pe5_configured_association_implementation'); discover('tests',pattern='test_pe5*.py'); established affected cross-phase suite; discover('tests',pattern='test_pe4*.py').
Final selection adds loadTestsFromName('test_pe6_classification_contract_design'), existing Asset/PE-5 suites and current-binding/cross-phase consumers; original hostname/manufacturer/core/monitoring/presentation/correlation fixtures are included as applicable.
Each run captures direct unittest result counts, failure/error/skip/class-skip totals and repository-byte/stash guards. No console truncation dependency.

Observed unchanged baseline counts (run/passed/failed/errors/skipped/class skips):

- assets: 27/27/0/0/0/0.
- focused: 84/84/0/0/0/0.
- pe5: 243/243/0/0/0/0.
- cross: 333/332/0/0/1/0.
- compatibility: 1905/1887/0/0/18/0.

Master Plan applicable passive-enrichment/source implementation policy: full native suite for source implementation. This task changes documentation, design governance and test bindings only; all product sources and accepted schemas are immutable. Runtime PE-6.1 must run full native suite.
Final observed candidate counts and exact selections will be recorded in the commit Evidence Report and final session report before publication, without mutating this already validated candidate to embed its own result. The governance baseline_results remain explicitly baseline evidence. No predicted counts or self-referential commit SHA is fabricated. Exact accepted commit/main-only push/independent GitHub identity/tree/blob comparison and clean main=origin are mandatory final publication gates.

## Original user authorization verbatim

The following complete normalized-LF text is preserved verbatim, not replaced by design summaries.
SHA256 of this exact UTF-8 normalized text: af837813ffff3bc64823810e17598808cca7608f840d864125a52b7b7f2ccedc. Original source is the user attachment in this session.

~~~text
# HIOC | PE-6: Classification & Metadata Quality
## Authoritative Contract Design, Architecture Review, and Execution Roadmap

**AUTHORIZATION:** Begin PE-6. Execute this entire repository investigation, contract-design, roadmap, and validation task without unnecessary intermediate approval gates.

**ACCEPTED PREDECESSOR:** PE-5 COMPLETE/PASS  
**BASELINE COMMIT:** `d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221`  
**PROJECT PHASE:** Phase 7A, Passive Living Inventory  
**NEXT CAPABILITY:** Classification & Metadata Quality  
**PRODUCTION ACCESS:** NONE

### 1. Permanent governing instructions

NO ASSUMPTIONS. EVER.

If a material fact is not established by authoritative evidence, it is UNKNOWN.

`UNKNOWN -> VERIFY -> ESTABLISH EVIDENCE -> DECIDE -> ACT`

Never use repository code, documentation, historical configuration, expected architecture, or naming conventions as proof of current production state.

Preserve original user instructions exactly. Do not paraphrase, weaken, omit, reinterpret, or silently replace them.

If new evidence conflicts with an established instruction, identify the exact conflict and STOP for resolution.

`docs/HIOC_MASTER_PLAN.md` remains authoritative.

Do not invent a new governance hierarchy or discard existing project conventions.

### 2. Working model

This is one authorized Codex repository task.

Perform the complete investigation, architectural analysis, contract design, roadmap documentation, testing, and Git closure that the established authority permits.

Do not stop for routine repository inspections, design comparisons, documentation edits, tests, commits, or verification.

Stop only for a genuine blocker, unresolved material decision requiring operator authority, prohibited operation, failed validation, or successful completion of the authorized task.

Maintain detailed evidence internally while producing a concise final Evidence Report.

### 3. Access restrictions

Work exclusively in the Windows HIOC repository.

Codex has no authenticated access to PI3.

Do not SSH into PI3, inspect PI3, synchronize its source repository, deploy to PI3, or access production.

Do not access PI5, Home Assistant, MQTT brokers, credentials, or private runtime state.

Do not execute any production collectors, association producers, schedulers, or inventory writers.

Do not alter production state.

Do not begin PE-7 or any later roadmap phase.

Preserve the accepted source/deployment separation:

- Windows development repository.
- `/home/jazofv1/hioc-release-source`: PI3 Git source.
- `/home/jazofv1/hioc`: PI3 production, deliberately non-Git.

### 4. Establish the exact baseline

Before modifications, independently verify:

1. Repository branch and HEAD.
2. Remote tracking status.
3. Clean or otherwise fully accounted-for working-tree state.
4. Accepted PE-5.9 completion commit and lineage.
5. PE-5 COMPLETE/PASS.
6. PE-6 NOT STARTED at the accepted baseline.
7. Current Master Plan authority.
8. Existing protected artifact boundaries.
9. Existing PE-6 references, future requirements, and dependencies.

Do not clean, reset, overwrite, or discard pre-existing changes.

If baseline authority cannot be established, STOP.

### 5. Comprehensive existing-capability inventory

Inspect the actual repository before designing anything new.

Identify the existing:

- Device identity and reconciliation models.
- Asset Foundation models introduced by PE-2.
- Manufacturer enrichment introduced by PE-3.
- Home Assistant association evidence introduced by PE-4.
- Service and MQTT relationship evidence introduced by PE-5.
- Known-infrastructure metadata sources.
- Operator-maintained metadata mechanisms.
- Inventory schemas and validators.
- Private and public projection boundaries.
- Existing role, type, category, classification, confidence, suggestion, provenance, and metadata-quality concepts.
- Dashboard representations and consumers.
- Persistence, history, and API contracts.
- Relevant unit, contract, integration, and regression tests.

Do not assume that a field or capability exists merely because the roadmap mentions it.

Distinguish:

- Implemented and validated.
- Implemented but unverified.
- Designed but not implemented.
- Planned.
- Historical or superseded.
- Unknown.

Provide exact file, schema, and test references supporting the classification.

### 6. Establish authoritative PE-6 requirements

Review the complete Master Plan and related historical decisions.

Recover the original PE-6 purpose, requirements, architectural intentions, dependencies, constraints, and acceptance expectations.

Pay particular attention to:

- Asset-centric Living Inventory.
- `role_suggestion`.
- `metadata_quality`.
- Device versus Asset distinction.
- Observation versus operator knowledge.
- Stable identity and provenance.
- Classification of devices with incomplete evidence.
- Unknown and ambiguous devices.
- Asset criticality and expected availability.
- Future permanent IoT monitoring.
- Future functional-impact and technical-dependency capabilities.
- Retention and archival dependencies.

Do not silently promote planned later-phase features into PE-6.

Where the current authority does not specify a technical decision, document it as an unresolved design decision and evaluate options.

Design recommendations must be clearly identified as proposals, not established facts.

### 7. Classification authority and semantics

Design a complete classification contract using the actual existing models.

Determine which classification mechanisms should be:

- Deterministic from authoritative evidence.
- Suggested from passive evidence.
- Explicitly approved by the operator.
- Unknown due to insufficient evidence.
- Conflicted or ambiguous.

Investigate appropriate roles for device type, manufacturer information, observed services, Home Assistant associations, configured MQTT relationships, and operator-maintained asset metadata.

Do not treat a manufacturer match, port, MQTT association, hostname, or Home Assistant association as automatic proof of a physical asset's identity or purpose.

Do not allow classification to mutate stable device IDs, canonical IP selection, network liveness, health, or incident state.

Propose exact precedence and conflict rules only after evaluating the existing authority model.

Distinguish operator-confirmed classification from unconfirmed role suggestions.

Explicitly preserve existing operator-approved values where the current schema grants them authority.

### 8. Role suggestion contract

Establish the requirements and proposed semantics of `role_suggestion`.

Analyze:

- Candidate input signals.
- Allowed and prohibited inference sources.
- Deterministic rule evaluation.
- Suggestion provenance.
- Strength or confidence representation, if warranted.
- Missing evidence.
- Multiple competing suggestions.
- Rule conflicts.
- Manual overrides.
- Source changes.
- Stability across inventory cycles.
- Privacy.
- Explainability.
- Consumer behavior when suggestions are unavailable.

Do not invent numerical confidence thresholds without a justified contract.

A suggested role must not silently become an operator-confirmed classification.

Do not create false certainty from multiple correlated sources that ultimately originate from the same evidence.

### 9. Metadata quality contract

Establish what `metadata_quality` is intended to represent.

Evaluate whether it should measure completeness, evidence reliability, operator confirmation, provenance quality, or some explicitly separated combination.

Do not collapse fundamentally different concepts into an unexplained score.

Investigate quality implications of:

- Strong versus weak identity.
- Known versus unknown manufacturer.
- Operator-approved friendly name.
- Physical location.
- Device purpose.
- Confirmed classification.
- Unconfirmed role suggestion.
- Accepted service associations.
- Missing or conflicting metadata.
- Stale evidence.
- Source provenance.
- Metadata that is intentionally not applicable.

If proposing scores, grades, flags, or quality categories, establish deterministic definitions and explain their limitations.

Do not treat metadata quality as device health or network availability.

### 10. Asset-centric compatibility

Review the existing PE-2 Asset Foundation and preserve its exact accepted contract.

Determine how PE-6 should relate devices and operator-managed assets without presupposing that the existing schema supports every envisioned field.

Consider the longer-term asset model:

- Friendly name.
- Physical location.
- Purpose.
- Owner or responsible person.
- Asset classification.
- Operational criticality.
- Expected availability.
- Notes and maintenance context.
- Lifecycle state.
- Multiple discovered identities belonging to one operator-confirmed physical asset.

These are architectural considerations, not automatic authorization to implement all fields in PE-6.

Clearly separate features necessary for PE-6 classification from future Asset management, PE-7 monitoring, retention, and maintenance workflows.

No heuristic merging of stable identities.

Any future linkage across randomized or rotated MAC addresses must require the appropriate operator authority and separately accepted identity model.

### 11. PE-5 private handoff integration

Review the accepted PE-5.9 private handoff contract completely.

Determine how PE-6 may consume validated, confirmed, unexpired private relationship evidence.

Preserve all required:

- Schema validation.
- Source identity.
- Revision and digest semantics.
- Durability confirmation.
- Evaluation and expiry.
- Missing, stale, invalid, and failed input handling.
- Relationship provenance.
- Privacy boundaries.
- Safe rejection behavior.

PE-5 service relationships are descriptive associations.

They do not establish identity, canonical IP, liveness, health, physical location, or confirmed asset classification.

Do not modify the accepted PE-5 implementation as part of this contract-design task.

### 12. Complete design decisions before implementation

Produce an evidence-backed PE-6 technical design covering:

1. Exact inputs and their authority.
2. Required output semantics.
3. Private versus public data boundaries.
4. Schema and versioning strategy.
5. Classification precedence.
6. Role suggestion rules.
7. Metadata quality representation.
8. Operator confirmation and overrides.
9. Missing/conflicting/stale input behavior.
10. Deterministic processing and stable outputs.
11. Provenance and explainability.
12. Privacy and credential handling.
13. Storage and retention implications.
14. Producer and consumer boundaries.
15. Compatibility with existing inventory.
16. Failure handling.
17. Restart and recovery implications.
18. Required test fixtures.
19. Deployment implications.
20. Rollback and production acceptance requirements.

For each material decision, record:

- Existing authority.
- Available alternatives.
- Rationale.
- Compatibility implications.
- Selected or proposed disposition.
- Required evidence.
- Whether operator approval is needed.

Do not claim a proposal is already authorized by previous work unless the source establishes it.

### 13. Determine the complete PE-6 execution sequence

Using the actual scope and technical dependencies, produce a clear, efficient set of PE-6 checkpoints.

Use the fewest boundaries that preserve meaningful distinctions between:

- Contract design.
- Implementation and repository validation.
- PI3 source synchronization.
- Production deployment.
- Bounded production execution.
- Independent acceptance.
- Final governance closure.

These are considerations for selecting a sequence, not instructions to manufacture seven separate checkpoints.

Combine tightly related tasks when they share the same authority and risk boundary.

Keep production deployment and production execution separate wherever evidence or mutation risk requires it.

Do not introduce unnecessary micro-checkpoints or repeated approval gates.

Every checkpoint must identify:

- Objective.
- Scope.
- Dependencies.
- Inputs and outputs.
- Access boundaries.
- Allowed changes.
- Tests.
- Acceptance criteria.
- Operator action, if necessary.
- Stop conditions.
- Exact successor.

Resolve design unknowns at the appropriate stage rather than allowing them to become uncontrolled implementation assumptions.

### 14. Documentation and governance

Update existing authoritative documentation as appropriate for this PE-6 contract-design task.

At minimum evaluate:

- `docs/HIOC_MASTER_PLAN.md`
- `ROADMAP.md`
- `docs/DATA_MODEL.md`
- `docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md`
- Relevant existing PE-5 handoff references.
- Existing governance records and schemas.
- Relevant tests for documentation and current-consumer consistency.

Use established classifications:

`CURRENT`  
`HISTORICAL_INTENTIONALLY_PRESERVED`  
`STALE_REQUIRES_UPDATE`

Preserve historical evidence exactly.

Do not introduce a competing Master Plan or duplicate existing governance.

The current PE-5 acceptance remains immutable.

### 15. Validation

Determine required validation from the current repository and applicable governance.

Run focused tests covering:

- PE-6 requirements and design consistency.
- Existing Asset Foundation boundaries.
- PE-5 handoff compatibility.
- Documentation/governance integrity.
- Historical/current lifecycle semantics.
- Privacy and protected invariants.
- Relevant cross-phase references.
- Roadmap sequencing.

Run broader regression tests where applicable.

Determine whether the full native suite is required based on the actual files changed and authoritative test policy.

Report exact commands, counts, failures, errors, skips, and limitations.

Do not silently waive required validation.

### 16. Commit and independently verify

If the authorized design work passes:

1. Update the Master Plan and relevant existing documents.
2. Record precise PE-6 design decisions and unresolved operator decisions.
3. Establish the approved or proposed execution sequence without claiming implementation.
4. Confirm PE-5 remains COMPLETE.
5. Ensure no runtime implementation or production mutation occurred.
6. Run all required tests.
7. Verify protected invariants.
8. Commit the authorized design/documentation/governance changes.
9. Push to main.
10. Independently retrieve the GitHub commit and verify it matches the accepted local candidate.
11. Verify clean working tree and HEAD equals origin/main.
12. Preserve existing stash state.

Do not start a later implementation or production checkpoint as an implicit continuation of this design task.

### 17. Stop conditions

STOP if a material requirement cannot be established, if existing authority conflicts with the proposed design, or if an operator decision is essential before a safe design can be completed.

STOP for failed validation, protected changes, privacy violations, unexplained repository divergence, or inaccessible authoritative evidence.

Do not fabricate missing requirements or use guesses to close a design gap.

If a blocker occurs, preserve completed safe work and report the exact reason.

### 18. Required Evidence Report

Return the actual observed results for:

`RESULT`  
`CHECKPOINT`  
`BASELINE_COMMIT`  
`PE5_STATUS`  
`PE6_STATUS`  
`REQUIREMENTS_RECONCILIATION`  
`EXISTING_CAPABILITY_INVENTORY`  
`CLASSIFICATION_CONTRACT`  
`ROLE_SUGGESTION_CONTRACT`  
`METADATA_QUALITY_CONTRACT`  
`ASSET_FOUNDATION_COMPATIBILITY`  
`PE5_PRIVATE_HANDOFF_COMPATIBILITY`  
`UNRESOLVED_DECISIONS`  
`EXECUTION_ROADMAP`  
`DOCUMENTATION`  
`PROTECTED_INVARIANTS`  
`FOCUSED_TESTS`  
`AFFECTED_TESTS`  
`REGRESSION_TESTS`  
`FULL_SUITE_DISPOSITION`  
`TEST_FAILURES`  
`TEST_ERRORS`  
`FILES_CHANGED`  
`COMMIT`  
`PUSH`  
`INDEPENDENT_GITHUB_VERIFICATION`  
`WORKTREE`  
`HEAD_EQUALS_ORIGIN_MAIN`  
`NEXT_CHECKPOINT`  
`PRODUCTION_ACCESS`  
`PRODUCTION_MUTATION`  
`STOP_REQUIRED`

Do not report expected results as observed results.

**Execute this entire PE-6 contract-design and execution-roadmap task in one Codex session. Stop only at a genuine blocker or completed, validated design checkpoint. Do not implement PE-6 runtime behavior or initiate production work under this authorization.**
~~~
