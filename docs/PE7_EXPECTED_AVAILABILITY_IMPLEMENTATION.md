# PE-7.1 Expected Availability repository implementation

Status: PE-7.1 COMPLETE/PASS; independent focused recheck ACCEPT. Repository implementation only; no production permission.

The final governance disposition below supersedes preparation-time status and next-action labels.
Earlier narratives remain historical evidence, including the original independent REJECT.

## Historical implementation preparation and validation narrative
Baseline: `ad9ddc5ced903f8c922a12c08f843fba6fce907b`, main, synchronized and clean
before mutation. The accepted [PE-7 contract](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md)
had original accepted baseline SHA-256
`57534e84132f4b305608dd1492462b9581e646228bef3bbf0cb47b9b9607f617`.
The separately authorized bounded PE-7.1 correction now adds section 6.1: an
authenticated read-only availability-status interface resolving T03 evidence scope
and T04 specific missing/stale reasons without requiring an incident. The existing
policy response and case summary cannot supply these facts. No implementation was
changed by that documentation-only correction. Its pause was subsequently lifted
by the explicit PE-7.1 resumption authorization; implementation now includes the
section 6.1 read interface. No later checkpoint or Git publication was authorized. Original
accepted mutation, qualification, lifecycle and dispatch contracts remain intact.

## Scope and ownership

One Windows repository candidate covers Asset schema 2.0, explicit migration and
rollback, version-aware PE-6 reading, the authenticated HA service bridge and local
editor, qualified observations/evaluation, and existing incident-engine cases and
dispatch. No independent acceptance, commit or push has occurred. PE-7.2 is not
started or authorized. No production configuration, credentials, numeric operational
profiles, eligible Assets, source mappings, recipients or schedule is selected here.

The finite pre-mutation manifest captures every baseline path's SHA-256, Git blob
and mode. The candidate record binds final implementation artifacts and protects
every other baseline path. The original implementation scope extension is mqtt.py: its
existing methods remain unchanged; the new opt-in transport supplies an absolute
deadline, numeric broker address, one QoS1 attempt, PUBACK evidence and no retry or
offline queue. Existing telemetry/legacy notification behavior retains its authority.

## Asset transactions and compatibility

The legacy 1.0 validator remains strict. The separate 2.0 validator closes the
store, record and durable receipt schemas. Policy fields preserve null/explicit
OFF, independent toggles, inactive type and policy-only records. AssetService owns
all writes to the same assets.json under its existing lock. Migration requires an
explicit local command, stopped writers and the exact source digest. Rollback
requires stopped writers and explicit retention of later edits, preserves an exact
private backup, restores exact 1.0 bytes, and rotates an epoch when restoring 2.0.

The Asset-local assets_transaction_status.json is durability evidence, not another
policy or nonce store. PREPARED is persisted before replacement. CONFIRMED binds
the exact store/status hashes only after both replacements and parent fsyncs
succeed. The Asset status schema remains unchanged. A missing, PREPARED, corrupt or
mismatched witness cannot establish completion. Explicit read-only reconciliation
may verify an already completed pair; it never repairs files or retries mutation.
An uncertain write remains COMMIT_UNKNOWN. Receipts alone cannot prove durability.

PE-6 consumes original supported-version bytes/value/digest without a projection
or provenance relabeling. Policy does not infer roles, health or availability inside
classification. Historical governance tests replay their accepted Git checkpoint;
new PE-7 successor tests protect the current candidate separately. Original records,
schemas, historical function laws and production evidence remain immutable.

## Authentication, UI and evidence

HA services resolve the actual authenticated WebSocket connection, active non-system
admin, explicit operator allowlist, normal login refresh token and provider
validation for every request. Tokens remain in HA. Closed signed assertions bind
issuer, audience, actor, context, request, route, payload and expiration. The adapter
requires verified mTLS and the independently pinned client public key plus backend
actor/operation/Asset ACL. Service credentials alone do not authorize a person.

The local editor uses same-origin authenticated HA service responses, retains
drafts separately from confirmed values, requires explicit creation, blocks unsafe
identity attachment and revision conflicts, and offers read-only uncertain-result
reconciliation. Viewing or reload never creates an Asset. Live storage-managed
Dashboard delivery requires the later supported resource/card editor procedure;
copying repository YAML does not update it. No live .storage file is edited.

Profiles have no production defaults. Only distinct advancing producer reports
with approved identity, authority, scope, success, completeness and freshness can
qualify. Source absence, failure, DHCP assignment/expiry, passive absence, registry
membership or switch OFF cannot prove physical outage. Count and grace both apply;
recovery needs qualified positive reports. Unknown/stale freezes an existing case.

## Incident ownership and dispatch

Incident-engine-v2 remains the sole lifecycle writer. Its versioned PE-7 state
commits per-Asset cases and outbox together and preserves the authoritative legacy
active object separately from its derived display. Legacy no-candidate recovery
never consumes a PE-7 display as a legacy incident. Suppression is not recovery.
All cases remain available in the bounded, explicit operational summary.

The prospective PE-7 invocation uses the engine's internal transaction boundaries,
without the old external flock wrapper. An inherited outer lock is refused before
Asset acquisition. This does not change or activate any installed cron entry.
Normal evaluation releases Asset before incident work. Authorization/claim alone
use shared Asset guard then incident lock. No network operation holds either lock.

Authorization parent-fsync is the dispatch linearization point. OFF first denies
new grants; an earlier durable grant allows one attempt until the earlier of five
seconds or evidence expiry. Claim and submission are consumed durably. No automatic
retry follows unknown delivery or restart. Receiver dedup is persisted before HA
notification submission. PUBACK/HA service acceptance is not recipient delivery or
an exactly-once guarantee. Infrastructure never escalates initial warning severity.

## Validation evidence and limits

Established harness: bundled Windows Python, repository root, stdin unittest,
shell-free PATH, HIOC_TEST_SHELL removed, UTF-8 and no bytecode, with
`sys.path[:0]=['tests','pi4/lib']`. Counts are taken directly from unittest results.
Frontend tests execute the real local editor in Node with an explicit HA/DOM
fixture. HA identity tests use the reviewed 2026.8.1 API contract; they do not claim
an installed production HA version or physical human presence.

Earlier intermediate evidence, retained and superseded by final results below: 57 PE-7 tests passed; the two
Dashboard tests passed, including 11 executed JavaScript interaction cases. These
are not final acceptance totals. The first sandboxed Asset run failed to create
temporary fixture directories; the elevated native rerun supersedes it for product
validation, without deleting that historical failure. That intermediate run did not establish a full-suite PASS.

Windows native locking fixtures do not prove POSIX ownership, ACL or physical
power-loss durability. R repository evidence remains distinct from P bounded
production and A activation/natural-cycle evidence. All original PE-4/PE-5/PE-6
operator evidence and its limitations remain preserved.

The existing candidate is resumed under explicit authorization. Complete native
validation is complete as recorded below; one bounded independent implementation acceptance is next. No Git publication
or PE-7.2 action is authorized.


## Resumed candidate: section 6.1 and observation delivery

The corrected working-tree contract SHA-256 is
`db8e25ba10e7038ee56a66aa12481d11c18b731a22ee4dfdc4de761031a9e14d`.
The closed availability-status read has its own signed audience and exact Asset ACL,
separate 30/300 read quotas, bounded replies and sanitized errors. It reads secure
policy/evaluation/policy snapshots once without initializing locks/files, executing
evaluation or creating cases. A valid engine index distinguishes no evaluation from
unavailable storage. Existing incident-engine transactions retain evaluation evidence
for every evaluated Asset, including no-incident Assets, and preserve qualification
counters across cycles. Snapshot reason/scope/quality and actual policy epoch/revision
support T03/T04. The editor keeps saved policy, last applied revision and evaluated
state separate; cached results display actual times/deadlines and limitations.

HA observation submission is a separately configured service role, with its own
key/certificate/audience and exact Asset/source permissions. Explicit allowlisted
entity reads use actual last_reported, reviewed association membership and mapping.
No get-all-states, raw attributes, history, policy write or operator impersonation.
The integration retains an explicit collect-once callable; setup starts no collection,
timer, recurring activation or scheduler. The adapter wires the existing normalized
observation store. Actual trust, mappings, profiles and activation remain later P/A
facts; synthetic values are not selected production parameters.

Historical PE-6 raw-file fixture failure was reproduced. Git archive extraction
applied Windows checkout line endings while the immutable candidate record bound
exact Git bytes for two retained artifacts. The fixture now obtains those exact
accepted Git objects and requires their existing canonical AND file hashes before
materializing them in its temporary tree. The original assertion, recorded hashes,
class bodies and historical governance remain unchanged. Its exact rerun passed:
1 run, 1 passed, 0 failures/errors/skips. The final complete native run below also executes the historical governance consumers.

## Original fingerprint limitation and protected scope

The earlier documentation correction output omitted four pre-action fingerprints.
Their exact hashes captured at this resumption (not reconstructed historical proof):

| Path | Resumption SHA-256 |
| --- | --- |
| homeassistant/dashboards/hioc_dashboard_v2.yaml | 420291ebf0cf635568b7209b8d79f9db202bad5df2821e364f47b003cbbd53ae |
| homeassistant/packages/hioc_incident_center.yaml | eaf25b5e3b86bec554873d4e9e0a22e85d04554daaa10b264d6a0071140f0968 |
| pi4/bin/hioc-assets.py | 43d84f837243606ee58fb64f3febbc28f7766d05378045b42213c7adf48127ab |
| pi4/bin/hioc-incident-engine-v2.py | 20c488ed8680569ff0e0b5cc05fbc71906764cb564fcf3cb352e703701cae615 |

Their candidate changes are within the existing authorized CLI, incident-engine,
Dashboard and legacy-notification-exclusion scope. All four must be included in
independent code acceptance. Modification timestamps are not historical integrity
proof. The original limitation remains; no recovery exercise or historical hash is
invented. The original 458 protected baseline files have nine justified exceptions:
the explicitly authorized contract section 6.1 correction and eight directly affected
historical binding test adapters described below. The remaining 449 retain original Git blob/mode and raw byte identities. mqtt.py remains the
previously justified implementation scope extension for bounded dispatch transport.

## Repository acceptance coverage and limitations

T01/T02/T08..T11: Asset transaction and real editor fixtures (independent nullable
controls, explicit creation, retained type). T03/T04: status/engine/no-case fixtures
and editor rendering. T05/T06/T07: evaluator OFF plus B01..B12 suppression/episode
fixtures. T12/T13: stable-ID attachment, orphan/ambiguous refusal and existing Asset
identity regressions. T14: concurrent revision conflict and editor conflict fixtures.
B01..B12 deterministic barriers, deadline expiry, unknown delivery and restore epoch
remain mandatory, executed repository evidence rather than P/A delivery evidence.

C01..C06: Asset/evaluator/editor/compatibility; C07..C11: HA context, closed protocol,
replay/quota/TLS/actor ACL; C12..C19: transitions, source qualification, correlation,
cases/dispatch and editor truth; C20: full native regression and current/historical
bindings; C22's repository portion: synthetic overlap/expiry/restart and dispatch
barriers; C23's repository portion: protected baseline/privacy/cross-phase checks.
C21 and C24 production captures/independent acceptance, C22's natural cycles, installed
HA behavior, POSIX permissions/crash durability and actual recipient delivery remain
P/A gates, not satisfied by Windows synthetic execution. PE-7.1 is not COMPLETE/PASS
before its separate independent code acceptance. No production operation occurred.

Final candidate validation is PASS with the explicit unexecuted-test limitations below.
This is repository implementation-candidate readiness, not independent acceptance,
PE-7.1 governance closure, release publication or production permission.


## Required legacy-consumer scope reconciliation

The first complete native run finished without repository mutations: 3229 tests,
5 failure events and 40 error outcomes, 54 individual skips and five class-level
optional-PyYAML skips. Several error outcomes were subtests of the same test case;
the first harness derived its pass count by subtraction. Final runs count successful
test cases directly rather than treating subtest errors as separate tests.
Three errors were invocation failures because Windows PowerShell was omitted from
PATH. The corrected shell-free native PATH includes WindowsPowerShell/v1.0 and still
contains no POSIX shell; HIOC_TEST_SHELL remains cleared. No dependency installation.

Other failures were current/historical binding conflicts: old runtime-byte assertions
read the new Asset CLI/MQTT/Dashboard; old PE-4 protected-source validation admitted no
successor; the PE-5 runtime helper assumed every current implementation was still an
exact four-file PE-6 addition; and current lookups fell back to older PE-6 artifact
maps for protected-but-previously-updated documentation. These are not new production
observations, changed historical identities, or permission to relax original checks.

The contract requires immutable historical replay plus separate exact current
successor validation. Six additional test paths are necessary and justified under
the resumption authorization's contract-required exception allowance:

- tests/test_pe4_ha_association_independent_production_acceptance_preparation.py
- tests/test_pe4_ha_association_public_projection_deployment_closure.py
- tests/test_pe4_ha_association_public_projection_test_binding_correction.py
- tests/test_pe5_local_service_association.py
- tests/test_pe5_service_association_caller.py
- tests/test_pe6_classification_contract_design.py

Their original class methods and historical validator bodies remain intact. Five
historical current-byte assertions reuse the established immutable 9d6ce274 replay
fixture, retaining their original older Git comparisons. Legacy validator entry
wrappers first verify the complete current PE-7 candidate, then evaluate original
historical laws against that exact accepted snapshot. Current binding overlays include
the 39 current candidate artifacts plus only inherited artifact identities from
the established accepted PE-6.1 map, avoiding stale fallback maps without expanding
edit scope or admitting an arbitrary protected path. The fixture labels synthetic historical index/HEAD state explicitly;
it neither stages files nor claims that virtual state is the live repository.
Shared caches hold only immutable Git-object/ref commands, never current source,
HEAD, staging, ACL, branch or untracked-path observations.

At that repair stage, scope was 38 paths: the original 31 intended implementation paths, the separately
authorized corrected contract, and these six necessary binding adapters. All 451
remaining baseline paths were protected at that stage. No historical governance JSON/schema,
accepted receipt, deployment artifact or production evidence was rewritten.

The final robustness pass also bounds serialized incident state before replacement,
adds an oversized-state rejection fixture, persists direct 1.0/2.0 classification
and native Reader provenance fixtures, and extends actual Node editor tests to 17
interaction cases covering T03/T04, expiry, pending revision and unavailable reads.
These are existing C04/C09/C12/C19 obligations, not new acceptance criteria.


### Final actor-proof lifetime boundary

The second full-suite attempt was explicitly interrupted for a security-source
correction; it has no final result and is not acceptance evidence. The HA bridge
had begun the 30-second assertion window in its executor, after actor verification.
A queued request could therefore extend the age of that verification. The handler
now captures the logical issuance time before verification/offloading; the signer
preserves that instant and exclusive deadline and denies expired/future proofs
before transport. Key-file I/O cannot renew the window. No assertion field, actor
architecture, user permission, source TTL or production policy changes. A deterministic
fixture covers admission at 29 seconds, rejection at 30/31 seconds, backward clock,
unchanged payload and absence of network submission after expiry.


### Third complete native result and two additional historical consumers

The completed third native run recorded 3236 tests, 3190 direct successes,
two failures, zero errors, 44 individual skips and five class-level skips;
2898.657 seconds. The pre/post repository snapshot reported no file changes.
This failed result is preserved and is not candidate acceptance. Two original
historical assertions compared current MQTT/Dashboard bytes to immutable PE-4
predecessors:

- tests/test_pe4_ha_association_public_projection_preparation.py: PreparationGovernanceTests.test_bound_sources_exact_git_and_immutable_runtime
- tests/test_pe4_ha_runtime_credential_provisioning_closure.py: CredentialClosureTests.test_protected_sources_no_adapter_and_document_links

Their recorded predecessors remain authoritative for those historical checkpoints.
PE-7 requires the Dashboard controls and bounded dispatch transport, so reverting
those current implementations would violate its contract. These two modules now
reuse the established immutable historical replay selector for only those methods.
Original assertion/class bodies, historical records/schemas, Git objects and
expected identities are unchanged. The current candidate is checked separately
before replay. This is the same contract-required successor exception, not a
production exemption or relaxed historical law.

Final scope is now 40 paths (18 tracked modifications, 22 new files), with eight
historical test-adapter exceptions plus the already authorized corrected contract.
The other 449 original baseline files remain protected. Earlier 38/451 scope
figures above describe the earlier candidate. Focused and complete native results
for the final candidate are recorded only after rerun.


The first combined rerun of the two corrected modules and all PE-7 tests recorded
189 run, 188 passed, one failure, zero errors/skips (365.125 seconds). The
projection-preparation assertion passed. The credential closure advanced to its
unnormalized source-hash check and exposed the same archive/check-out line-ending
representation distinction as the earlier PE-6 candidate fixture. Both existing
raw source bindings were independently verified against immutable 9d6ce274 Git
bytes and their recorded SHA-256 AND Git blob identities. Only that selected
historical fixture now materializes those two verified representations in its
temporary tree. No working-tree runtime file, original assertion, record, schema
or expected hash changes. This failed run remains evidence, not acceptance.

## Final native validation and candidate readiness

- Final focused PE-7 plus the two corrected historical modules: 189 run,
  189 passed, 0 failures, 0 errors, 0 skips; 393.641 seconds.
- This includes all 93 PE-7 tests (zero failures/errors/skips), all
  B01..B12 fixtures and 17 actual JavaScript interaction cases.
- Affected historical/current consumers: 442 run, 441 passed, zero failures/errors,
  one skip. This earlier run precedes the later actor-proof and historical-fixture
  corrections; the complete final native run validates the final source/test bytes.
- Complete selection: `unittest.defaultTestLoader.discover('tests')`.
- Final full native: 3236 run, 3192 directly counted successes,
  0 failures, 0 errors, 44 individual skips,
  5 class-level skips; 2778.594 seconds.
- Final result counts and tracebacks are recorded directly, independently of
  console truncation. The pre/post repository-file snapshot reports zero changes.
- Established native PATH includes Windows System32, Windows,
  WindowsPowerShell/v1.0 and Git/cmd, with no POSIX shell; HIOC_TEST_SHELL cleared.
  Bundled Windows Python stdin uses UTF-8 and bytecode suppression with
  `sys.path[:0]=['tests','pi4/lib']`.
- Source/test raw hashes are checked unchanged after this complete run. Subsequent
  edits only finalize existing evidence, current Master Plan status and their
  successor identities; focused binding/lifecycle checks are repeated.

Individual skipped-test reasons (unexecuted, not passes):

- 2: Actual Linux/POSIX gate pending on PI3
- 22: Bash is required
- 1: Linux directory-substitution integration requires POSIX directory identity
- 1: Linux exclusive-ingress primitive requires POSIX O_DIRECTORY/O_NOFOLLOW
- 1: Linux renameat2 integration fixture
- 1: PyYAML is not available in this Python runtime
- 4: descriptor-relative Action D filesystem semantics are PI3/POSIX-only
- 1: descriptor-relative hierarchy semantics are PI3/POSIX-only
- 1: real POSIX descriptor semantics require native validation
- 6: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- 1: rsync is not installed
- 1: symlink creation is unavailable
- 1: symlink fixture unavailable: Windows privilege error 1314 (native temporary fixture)
- 1: symlink unavailable

Class-level skips (outside tests run, not passes):

- `setUpClass (test_dashboard_dynamic_truth.DashboardDynamicTruthTests)`: PyYAML is not available in this Python runtime
- `setUpClass (test_dashboard_layout.DashboardLayoutTests)`: PyYAML is not available in this Python runtime
- `setUpClass (test_dashboard_severity.DashboardSeverityTests)`: PyYAML is not available in this Python runtime
- `setUpClass (test_inventory_presentation.InventoryPresentationTests)`: PyYAML is not available in this Python runtime
- `setUpClass (test_watch_device_presentation.WatchDevicePresentationTests)`: PyYAML is not available in this Python runtime

No optional dependency was installed. No POSIX or production result is inferred.
No unresolved test failure/error remains. Independent code acceptance has not
been performed. The candidate stays uncommitted/unstaged; PE-7.2 remains
NOT STARTED / NOT AUTHORIZED.

## Exact candidate path manifest

Complete scope: 40 uncommitted paths, comprising 18 existing tracked modifications
and 22 new files. The successor record binds 39 artifacts without a recursive
self-identity and protects the other 449 original baseline files. Original raw
hashes, Git blobs/modes and the unchanged corrected-contract hash are checked
separately from current successor artifacts.

- `docs/HIOC_MASTER_PLAN.md`
- `docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md`
- `docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md`
- `governance/pe7/pe7-implementation-candidate.json`
- `homeassistant/custom_components/hioc_operator/__init__.py`
- `homeassistant/custom_components/hioc_operator/manifest.json`
- `homeassistant/custom_components/hioc_operator/services.yaml`
- `homeassistant/dashboards/hioc_dashboard_v2.yaml`
- `homeassistant/packages/hioc_incident_center.yaml`
- `homeassistant/www/hioc-asset-editor.js`
- `pi4/bin/hioc-assets.py`
- `pi4/bin/hioc-availability-adapter.py`
- `pi4/bin/hioc-incident-engine-v2.py`
- `pi4/lib/hioc/asset_policy.py`
- `pi4/lib/hioc/assets.py`
- `pi4/lib/hioc/availability.py`
- `pi4/lib/hioc/availability_contract.py`
- `pi4/lib/hioc/availability_incidents.py`
- `pi4/lib/hioc/availability_observation.py`
- `pi4/lib/hioc/availability_protocol.py`
- `pi4/lib/hioc/availability_server.py`
- `pi4/lib/hioc/classification.py`
- `pi4/lib/hioc/mqtt.py`
- `tests/test_pe4_ha_association_independent_production_acceptance_preparation.py`
- `tests/test_pe4_ha_association_public_projection_deployment_closure.py`
- `tests/test_pe4_ha_association_public_projection_preparation.py`
- `tests/test_pe4_ha_association_public_projection_test_binding_correction.py`
- `tests/test_pe4_ha_runtime_credential_provisioning_closure.py`
- `tests/test_pe5_local_service_association.py`
- `tests/test_pe5_service_association_caller.py`
- `tests/test_pe6_classification_contract_design.py`
- `tests/test_pe6_classification_implementation.py`
- `tests/test_pe7_assets.py`
- `tests/test_pe7_binding.py`
- `tests/test_pe7_contract.py`
- `tests/test_pe7_dashboard.py`
- `tests/test_pe7_dispatch.py`
- `tests/test_pe7_evaluation.py`
- `tests/test_pe7_ha.py`
- `tests/test_pe7_security.py`

## Next action

One bounded independent implementation/code acceptance of this existing candidate,
including the four paths with the historical fingerprint limitation. No commit,
push, deployment, PI3/PI5 access, live monitoring, notification activation or
PE-7.2 is authorized by this candidate-completion action.

## Exact unexecuted individual test IDs

These 44 registered skips are not passes. The five skipped classes are listed
separately above; their methods are not counted in the 3236 tests run.

- `test_git_artifact_governance.GitArtifactGovernanceTests.test_deployer_rejects_dirty_wrong_commit_untracked_and_modified_source`: Bash is required
- `test_git_artifact_governance.GitArtifactGovernanceTests.test_deployer_reports_matching_blob_source_target_and_backup`: Bash is required
- `test_homeassistant_yaml.HomeAssistantYamlTests.test_homeassistant_yaml_files_parse`: PyYAML is not available in this Python runtime
- `test_manufacturer_cli.ManufacturerCliTests.test_sidecar_reader_rejects_symlink`: symlink creation is unavailable
- `test_network_probe_governance.NetworkProbeGovernanceTests.test_configured_pi5_reaches_probe_and_inventory_arguments`: Bash is required
- `test_network_probe_governance.NetworkProbeGovernanceTests.test_missing_home_assistant_ip_fails_without_exposing_credentials`: Bash is required
- `test_network_probe_governance.NetworkProbeGovernanceTests.test_shell_sources_parse`: Bash is required
- `test_network_probe_platform_contract.NetworkProbePlatformContractTests.test_available_bash_executes_all_original_assertions`: Bash is required
- `test_pe2_synthetic_backup_cleanup.CleanupTests.test_symlink_and_directory_rejected`: symlink unavailable
- `test_pe3_action4_resume_script.PE3Action4ResumeScriptTests.test_parent_shell_survives_harmless_failure_and_later_stages_do_not_run`: Bash is required
- `test_pe3_action5_deploy.PE3Action5DeploymentContractTests.test_action5a_parent_shell_survives_failure`: Bash is required
- `test_pe3_action5_deploy.PE3Action5DeploymentContractTests.test_parent_shell_survives_harmless_failure`: Bash is required
- `test_pe3_action5c_bootstrap.PE3Action5CBootstrapContractTests.test_parent_shell_survives_failure_and_later_steps_do_not_run`: Bash is required
- `test_pe3_action6_install.PE3Action6InstallContractTests.test_bootstrap_parent_shell_survives`: Bash is required
- `test_pe3_action6_install.PE3Action6InstallContractTests.test_child_script_failure_preserves_parent_shell`: Bash is required
- `test_pe3_action7_activation.PE3Action7ActivationContractTests.test_bootstrap_parent_shell_survives`: Bash is required
- `test_pe3_action7_activation.PE3Action7ActivationContractTests.test_child_script_failure_preserves_parent_shell`: Bash is required
- `test_pe3_action8_generation.PE3Action8GenerationContractTests.test_child_script_failure_preserves_parent_shell`: Bash is required
- `test_pe3_action8_generation.PE3Action8GenerationContractTests.test_invalid_bootstrap_input_preserves_parent_shell`: Bash is required
- `test_pe3_action8_generation.PE3Action8GenerationContractTests.test_operator_supplied_evidence_directory_is_rejected`: Bash is required
- `test_pe3_action8_validator_deploy.PE3Action8ValidatorDeployTests.test_parent_shell_survives_invalid_input`: Bash is required
- `test_pe3_action9_validation.PE3Action9ValidationTests.test_parent_shell_survives_invalid_input`: Bash is required
- `test_pe3_production_runbook.PE3ProductionRunbookSequencingTests.test_action3_and_action4_bash_parse`: Bash is required
- `test_pe3_production_runbook.PE3ProductionRunbookSequencingTests.test_action5_bash_parses`: Bash is required
- `test_pe3_production_runbook.PE3ProductionRunbookSequencingTests.test_resume_prerequisite_preserves_parent_shell`: Bash is required
- `test_pe4_action_b_transfer.PE4ActionBTransferTests.test_linux_ingress_primitive_real_success_and_all_collision_types`: Linux exclusive-ingress primitive requires POSIX O_DIRECTORY/O_NOFOLLOW
- `test_pe4_action_b_transfer.PE4ActionBTransferTests.test_linux_renameat2_real_no_replace_and_source_consumption`: Linux renameat2 integration fixture
- `test_pe4_action_b_transfer.PE4ActionBTransferTests.test_linux_whole_directory_replacement_rejects_same_mode_owner_and_content`: Linux directory-substitution integration requires POSIX directory identity
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_named_child_create_then_idempotent_open`: descriptor-relative hierarchy semantics are PI3/POSIX-only
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_path_bound_ancestor_rename_away_is_rejected_as_name_lost`: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_path_bound_ancestor_replacement_is_rejected_as_name_substituted`: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_path_bound_leaf_removal_is_rejected_as_name_lost`: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_path_bound_leaf_rename_away_is_rejected_as_name_lost`: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_path_bound_leaf_replacement_is_rejected_as_name_substituted`: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- `test_pe4_action_d_hierarchy_prepare.ActionDHierarchyPreparationContractTests.test_posix_path_bound_unchanged_leaf_revalidates`: real path-bound directory semantics require POSIX no-follow and descriptor-relative operations
- `test_pe4_action_d_runtime.ActionDPosixFilesystemTests.test_descriptor_cleanup_unlinks_links_without_following_targets`: descriptor-relative Action D filesystem semantics are PI3/POSIX-only
- `test_pe4_action_d_runtime.ActionDPosixFilesystemTests.test_exclusive_child_retains_parent_and_inode_identity`: descriptor-relative Action D filesystem semantics are PI3/POSIX-only
- `test_pe4_action_d_runtime.ActionDPosixFilesystemTests.test_json_publication_is_confirmed_and_no_replace`: descriptor-relative Action D filesystem semantics are PI3/POSIX-only
- `test_pe4_action_d_runtime.ActionDPosixFilesystemTests.test_unexpected_venv_symlink_is_rejected_but_lib64_is_allowed`: descriptor-relative Action D filesystem semantics are PI3/POSIX-only
- `test_pe4_action_e_handoff.TraversalTests.test_real_posix_read_only_walk`: real POSIX descriptor semantics require native validation
- `test_pe4_ha_association_public_projection.PosixReaderTests.test_real_reader_complete_copy_and_shared_vs_exclusive_lock`: Actual Linux/POSIX gate pending on PI3
- `test_pe4_ha_association_public_projection.PosixReaderTests.test_real_symlink_hardlink_dirty_namespace_and_permissions`: Actual Linux/POSIX gate pending on PI3
- `test_pe4_windows_ssh_identity_provision.IdentityProvisionTests.test_real_windows_dangling_symlink_is_still_a_collision`: symlink fixture unavailable: Windows privilege error 1314 (native temporary fixture)
- `test_release.ReleaseScriptTests.test_git_exclusion_preserves_legitimate_hidden_files`: rsync is not installed


## Authorized HA reserved-state correction after independent REJECT

The independent review returned REJECT for one confirmed blocker: the HA bridge
excluded unknown/unavailable from its positive branch but allowed either reserved
state through a configured negative mapping. Fresh reports could produce OFFLINE
and OUTAGE_STARTED. The new regression reproduced both failures before repair
(3 tests: 1 passed, 2 failing reserved-state subtests, zero errors/skips).

The bridge now handles both reserved states before either mapping branch,
unconditionally retaining UNKNOWN/insufficient evidence. Three new tests exercise
actual normalization -> evaluator -> incident transitions. Each reserved state is
placed in accepted negative and positive mappings, with distinct reports at 0, 5,
15 and 25 seconds: UNKNOWN, zero negative/positive counts, no cases/outbox events.
Genuine connected/disconnected mappings retain AVAILABLE/OFFLINE and the genuine
OUTAGE_STARTED event. No evaluator, incident, dispatch, policy, Dashboard, contract
or historical validator is changed.

Post-correction targeted modules: 44 run, 44 passed, zero failures/errors/skips,
zero class-level skips, including all three new tests and B01..B12 fixtures.
Exact native configuration: repository-root working directory; bundled interpreter
C:\Users\JorgeAzofeifaCastill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -B -
with PowerShell stdin, PYTHONIOENCODING=utf-8, HIOC_TEST_SHELL cleared, and PATH
C:\Windows\System32;C:\Windows;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Program Files\Git\cmd

Exact unittest selections (TextTestRunner verbosity=2):
~~~python
sys.path[:0] = ['tests', 'pi4/lib']
# Before correction:
unittest.defaultTestLoader.loadTestsFromNames([
    'test_pe7_ha.ObservationRoleTests.test_reserved_unknown_mapping_cannot_create_outage',
    'test_pe7_ha.ObservationRoleTests.test_reserved_unavailable_mapping_cannot_create_outage',
    'test_pe7_ha.ObservationRoleTests.test_genuine_mappings_preserve_evaluation_and_outage_events'])
# After correction:
unittest.defaultTestLoader.loadTestsFromNames([
    'test_pe7_ha', 'test_pe7_evaluation', 'test_pe7_dispatch'])
# Binding/preservation, same native configuration:
unittest.defaultTestLoader.loadTestsFromName('test_pe7_binding')
~~~
The post-correction result directly counts addSuccess and records final counts
and source hashes in temporary hioc-pe71-ha-reserved-state-targeted-result.json.

Current corrected identities (raw SHA-256 / Git clean-filter blob):

- homeassistant/custom_components/hioc_operator/__init__.py: ebf4d61bdc2bdd1d5757d420c0fd520c08101ff665976d8128c105eb8ad2547d / aba3acac0b0674fbb6421026ab6832b67ce60ca8

- tests/test_pe7_ha.py: fa7e008c0566e7abac2bbf395be66039f6cd5f87347c4114ce487701a40c8963 / 188343966e64254884345cd2c04158c9d1705016

The previous 3236-test full native result applies to the prior candidate; it is
not a full-suite validation of corrected bytes. No full suite was rerun. Its 44
individual skips and five class-level skips remain unexecuted limitations.
The existing four-file historical fingerprint limitation remains documented;
current identities do not reconstruct missing historical proof.
Only the bridge, its tests, this document and their successor identities change.
The Master Plan remains unchanged; the revised candidate awaits focused independent
recheck. This correction is not independent acceptance or PE-7.1 COMPLETE/PASS.
All unrelated candidate bytes and 449 original protected files remain protected.
No commit, push, PI3/PI5/HA/production access, deployment or activation occurred.
Next action: focused independent recheck of this reserved-state correction.

Binding/preservation result: 7 run, 7 passed, zero failures/errors/skips and
zero class-level skips. This includes negative identity/scope/lifecycle fixtures
and preservation of original historical assertions and MQTT implementations.
Final static identity and scope verification is repeated after this evidence
addition and successor synchronization; no product/test bytes change afterward.


## Final PE-7.1 independent acceptance and governance closure

PE71_STATUS=COMPLETE/PASS; PE71_INDEPENDENT_ACCEPTANCE=ACCEPT.
PE71_FOCUSED_RECHECK=ACCEPT; PE70_STATUS=COMPLETE/PASS.
PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
Deployment result: NOT_DEPLOYED; repository implementation acceptance only.

The original independent review returned REJECT for the confirmed HA reserved-state
false-outage defect. The authorized repair returned
PE71_HA_RESERVED_STATE_CORRECTION=PASS. The focused independent recheck then
returned ACCEPT: unknown/unavailable are excluded before both mapping branches,
including accepted configurable meanings, and cannot independently establish
negative qualification, OFFLINE, OUTAGE_STARTED or its notification.
Genuine qualified positive/negative behavior remains intact. No other review was
reopened and no confirmed acceptance blocker remains. Earlier rejection, repair,
fingerprint limitations and test evidence above are preserved.

### Completed validation and limits

| Validation | Run | Passed | Failures | Errors | Individual skips |
| --- | ---: | ---: | ---: | ---: | ---: |
| Focused PE-7 before correction | 93 | 93 | 0 | 0 | 0 |
| Focused plus historical modules before correction | 189 | 189 | 0 | 0 | 0 |
| Full native before correction | 3236 | 3192 | 0 | 0 | 44 |
| HA/evaluator/incident correction | 44 | 44 | 0 | 0 | 0 |
| Binding/preservation correction | 7 | 7 | 0 | 0 | 0 |

The five additional class-level skips and exact individual/class reasons above
remain unchanged and unexecuted, not passes. The full 3236-test suite completed
before the HA correction and was not repeated afterward. The focused independent
recheck accepted the corrected source identities without another full suite.
No implementation tests are repeated during documentation/Git closure.
The corrected bridge SHA-256 remains
ebf4d61bdc2bdd1d5757d420c0fd520c08101ff665976d8128c105eb8ad2547d
and Git blob aba3acac0b0674fbb6421026ab6832b67ce60ca8.
The corrected HA test SHA-256 remains
fa7e008c0566e7abac2bbf395be66039f6cd5f87347c4114ce487701a40c8963
and Git blob 188343966e64254884345cd2c04158c9d1705016.
The corrected accepted contract remains SHA-256
db8e25ba10e7038ee56a66aa12481d11c18b731a22ee4dfdc4de761031a9e14d;
its original accepted identity and authorized section 6.1 extension remain above.

### Preservation and publication boundary

The exact existing 40-path manifest remains the publication scope, with 39
successor artifact identities and 449 protected original files. Closure changes
only current Master Plan governance, this Evidence Report and their corresponding
current identity fields. No implementation source/test is regenerated or changed.
All historical records, original test assertions and accepted Git objects remain
preserved. The existing four-file historical fingerprint limitation remains:
current fingerprints do not reconstruct unavailable historical observations.

The successor record retains its frozen implementation-candidate metadata and
baseline for historical candidate validation; the current Master Plan and this
final disposition own subsequent independent acceptance and governance closure.
Its two documentation identities follow these authorized final document bytes.
Publication uses one exact 40-path commit, normal main push, independent remote
identity verification and a clean synchronized checkout. The resulting commit
identity and observed publication outcome are reported after these gates; no
self-referential commit SHA or unobserved push success is embedded here.

No PI3/PI5, Home Assistant, MQTT, credentials or production access occurred.
No deployment, integration installation, Asset migration, monitoring, scheduling
or recurring activation occurred. No production functionality is claimed.
PE-7 is not complete.

NEXT_CHECKPOINT=PE-7.2 - Operator-only exact release-source synchronization.
PE72_STATUS=NOT_STARTED; PE72_AUTHORIZED=FALSE.
Exactly one next checkpoint requires separate authorization: operator-only exact
release-source synchronization, without runtime delivery, migration or execution.
STOP after the authorized repository closure and publication gates.


## PE-7.2 release-source synchronization acceptance and governance closure

PE72_STATUS=COMPLETE/PASS; DEPLOYMENT_RESULT=SOURCE_SYNCHRONIZATION_ONLY.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS.
PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
All production/source-checkout observations below are OPERATOR_SUPPLIED.
Codex made no PI3 or PI5 connection. No observation timestamp, process exit code,
tree hash or historical runtime comparison is invented.

### Exact supplied synchronization evidence

Target PI3 NUT&PIHOLE; hostname nutandpihole.
Source checkout /home/jazofv1/hioc-release-source; remote
https://github.com/jorgeazofeifa-creator/hioc.git.
Before synchronization: branch main, commit
1477f672db00e67bc1923a667a8dd5913f183166, clean tree, no stashes,
target commit initially absent locally.
The operator performed git fetch --prune origin main and verified origin/main
51398bab4e2293b578b2cdac2d0740c3738cab2f; local branch 0 ahead / 4 behind,
fast-forward eligible.
The operator performed
git merge --ff-only 51398bab4e2293b578b2cdac2d0740c3738cab2f.
Observed fast-forward completion synchronized exactly 40 PE-7.1 paths;
final HEAD equals accepted source commit
51398bab4e2293b578b2cdac2d0740c3738cab2f, branch tracks origin/main,
and working tree is clean.

IMMUTABLE_REPOSITORY_FACT: Windows Git objects independently establish the
start as ancestor, exactly four intervening commits, and a 40-path endpoint
change set. These facts corroborate the supplied sequence; they do not independently
observe the PI3 filesystem or authenticate the operator transcript.

### Exact isolation observations and limits

OPERATOR_SUPPLIED: /home/jazofv1/hioc exists and is not a Git worktree.
The following exact runtime paths were observed ABSENT:
- /home/jazofv1/hioc/pi4/lib/hioc/availability.py
- /home/jazofv1/hioc/pi4/lib/hioc/availability_server.py
- /home/jazofv1/hioc/pi4/lib/hioc/asset_policy.py

The synchronization command targeted only /home/jazofv1/hioc-release-source.
These observations establish successful source synchronization and absence of the
three checked new modules. They do not establish historical byte-for-byte
production preservation, absence of every possible runtime artifact, a comprehensive
production-service audit, current production health or operational PE-7 acceptance.
No Codex production access, deployment, HA integration installation, services,
credentials, Assets, monitoring, scheduling or notification action occurred.

### Repository closure and unchanged acceptance authority

Documentation-only closure updates the current Master Plan, this existing evidence
document and only their directly affected successor artifact identity fields.
Accepted PE-7.1 source/tests and the corrected contract remain unchanged.
Original rejection/correction/focused ACCEPT, exact source identities, native/targeted
test history, all skip reasons and the four-file historical fingerprint limitation
above remain preserved. No native implementation suite is rerun for this checkpoint.
Static documentation/reference/lifecycle, exact path, protected-identity and
git diff --check verification gate publication. Exact commit, normal main push,
independent remote identity and clean checkout are verified and reported afterward.
The prior implementation-candidate metadata retains its historical meaning;
current lifecycle authority is the Master Plan and this PE-7.2 disposition.
PE-7 remains IN_PROGRESS.

NEXT_CHECKPOINT=PE-7.3 - Guarded artifact, integration, UI and trust delivery.
PE73_STATUS=NOT_STARTED; PE73_AUTHORIZED=FALSE.
Separate authorization is required. No PE-7.3 delivery or automatic follow-on
action begins here. Later migration/execution and activation remain separately gated.
