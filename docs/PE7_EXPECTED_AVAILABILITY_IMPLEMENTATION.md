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


## PE-7.3 guarded PI3 delivery transaction repository candidate

PE73_STATUS=IN_PROGRESS_REPOSITORY_PREPARATION.
PE73_PI3_DELIVERY_CANDIDATE=PARTIAL; NATIVE_LIVE_COMMIT=BLOCKED_CONSUMER_COORDINATION_NOT_ESTABLISHED.
This is an uncommitted Windows implementation candidate for independent review,
not production delivery authority or PE-7.3 COMPLETE/PASS. No new phase/checkpoint
is created. Accepted PE-7.1 runtime source and contract bytes remain unchanged.

### Supplied production baseline and immutable source authority

Release artifacts are pinned to 51398bab4e2293b578b2cdac2d0740c3738cab2f.
Repository preparation baseline is d64d772f82728a41d920eb64433ee2398645097f.
PI3 hostname nutandpihole, UID:GID 1000:1000, five existing regular single-link
replacement files and eight absent targets are OPERATOR_SUPPLIED observations.
Every target is freshly validated at preparation and again before any synthetic
publication; prior preflight success never authorizes later publication.

The production MQTT baseline d55a174bec05cf009038bbd15ac911dd18039bddc56da1c9847b67bc81c65ff5
is exact historical Git blob d185aee1c3a30de72f060c824878224022236c3c. It differs
from the immediate pre-PE7 source MQTT file; no current-source substitution or
invented line-ending conversion is used to reconstruct its fixture bytes.

Exact payload below. Runtime modes preserve the five supplied existing policies.
New modules use private 0600 following PE-6 disabled installation; the new explicit
operator entry uses 0700 following the observed private Asset CLI precedent.
These are proposed delivery policies, not claims that new targets exist.

| Runtime-relative path | Accepted source SHA-256 | Accepted Git blob | Delivery mode |
| --- | --- | --- | --- |
| pi4/bin/hioc-assets.py | 43d84f837243606ee58fb64f3febbc28f7766d05378045b42213c7adf48127ab | 0b4d8bfdbf432dbed6ef62add9da73c74764c574 | 0700 |
| pi4/bin/hioc-availability-adapter.py | d53114faf5d3cddf6666716871f3f5b51a3876ea7db68b6ce0ab1379b0334ed7 | d81c5c7add4a682664897c99574ad2fa05d04bfa | 0700 |
| pi4/bin/hioc-incident-engine-v2.py | 6e9ec9d591ae2e48d19825c095aceb54542405329c842e271a367094475ffffe | f1a2423919edd609a79e8bbf4dfd574c98fee30e | 0755 |
| pi4/lib/hioc/asset_policy.py | 565e2314c8947a17e31e327b21960db4338e37f514ab7c3df31738006d178a2f | 917f23cc41487da7a68c2427b3af605e885616e2 | 0600 |
| pi4/lib/hioc/assets.py | 5a06d401c7496871c878337a32ec85a37dae53ba7e74fe97e30446f4d720f3ac | 132c572d875d8b87ae0d89b72eec2c69ddd1b57b | 0600 |
| pi4/lib/hioc/availability.py | 8b10bf0ced9e280a0d634fe4ec0082d6f267c1a5fd8c8abcae34e5660b2ba54d | c56a2c29fa712609adc9121d48c1639b69b818ba | 0600 |
| pi4/lib/hioc/availability_contract.py | b27f422e6badd13aefff5f75c1dfd03859f60b927be02721c95e56f18b4eaef3 | 1479d5c553608b6ceafc14e9553c7aa8f8839de1 | 0600 |
| pi4/lib/hioc/availability_incidents.py | f3d700b10b1de607dd32a36603bd6399a956450fa0a0eb75def4491567a39f5f | d765e77eb9b8442db97c0435f72a0ffe00142584 | 0600 |
| pi4/lib/hioc/availability_observation.py | 16722847de9d0a44097d82fffa1056a94efefb9b3eeac3e955336574db324ac0 | 6fe80ab1ea94a458db723c7ceabd4355fe07b8f0 | 0600 |
| pi4/lib/hioc/availability_protocol.py | 3245db6e1e05cd247095031d516d376298dbab8c33e6668548b5e0321350472b | b0398c151bec35671b76cc4f9cd343e59efe9557 | 0600 |
| pi4/lib/hioc/availability_server.py | 406cb71e787eafee6c1c780f70167449a9196eacdfe8222fa1cce66312952ab2 | efe0aa0da94f8fbce9b62395b28673dbde1dada4 | 0600 |
| pi4/lib/hioc/classification.py | 003ccb0eaead3476b85b8e2458d39199a84b439006f165f3fec8341c41a6eaa1 | c69c533e46a352dd498813c50fa680cfb57db84f | 0600 |
| pi4/lib/hioc/mqtt.py | 126cfcc6c6780be79e8ed6c1ce7b27f4088edfde7221794ced62bf31e24095d4 | 369a0efbbebea9d24ed571fe9210562feaddb464 | 0644 |

### Exact interface and safe defaults

Tool: tools/hioc-pe73-pi3-delivery.py. No action is implicit; argparse requires one
of preflight, inspect, prepare, commit, verify, rollback. These are interface
specifications, not an authorized operator production command or delivery block:

- preflight: read-only target/source/ancestor/metadata and actual crontab checks;
  prints the observed baseline and canonical preflight_sha256.
- inspect: read-only, idempotent secured journal inspection and separate current
  target matches. Missing journal in an existing transaction is INCOMPLETE, never
  proof of an untouched runtime.
- prepare --authorization REFERENCE --evidence-sha256 PREFLIGHT_SHA256:
  independently declared operator authorization plus exact fresh preflight binding;
  creates private backups/staging only, not live runtime artifact replacement.
- commit --authorization REFERENCE --evidence-sha256 JOURNAL_SHA256:
  independent fresh authorization and bound PREPARED journal; no automatic
  transition from preflight/prepare. Native CLI currently always refuses before
  live writes because consumer coordination is not established.
- verify: static installed-set verification only; never imports/executes payload.
- rollback --authorization REFERENCE --evidence-sha256 JOURNAL_SHA256:
  separate authorization, exact proven targets and backup bytes; native CLI
  currently refuses under the same consumer-coordination gate.

Authorization references are explicit local operator declarations, not authenticated
permission tokens or substitutes for separate human authorization. There is no
unsafe override, caller-supplied coverage boolean, receipt-as-permission, automatic
retry, resume/adoption or automatic rollback. No root/source path CLI override.
Native execution requires POSIX, hostname nutandpihole and real/effective UID/GID
1000; no sudo. The source gate uses /usr/bin/git with bounded subprocess calls,
controlled environment, exact release HEAD, root, remote URL, clean checkout and
all 13 immutable object SHA/blob identities. No Git network operation is performed.

The controller itself is newly prepared and is not part of the frozen PE-7.1
release. Its eventual reviewed publication/runner provenance and delivery must be
separately established before any operator use. No production command is issued here.

### Transaction, backups, metadata and failure states

Proposed private namespace: backups/pe73-pi3-delivery-v1; its actual production
absence is UNKNOWN and never assumed. Existing namespace/journal stops preparation.
No historical PE-4/PE-5/PE-6 transaction directory is removed, renamed or adopted.

Descriptor-based no-follow traversal validates absolute ancestors and pins
directory/name identities. Bounded reads reject non-regular objects, hard links,
unsafe owner/mode or POSIX ACLs. Original file type, SHA, UID/GID, mode, link count,
device/inode, timestamps and ancestors are retained in the baseline journal.
All five replacement bytes are backed up privately before any live mutation;
13 Git-object payloads are staged and verified. Directory mode 0700, journal,
backup and stage mode 0600; file and directory fsync barriers precede progress.

The finite journal states are PREPARING, PREPARED, COMMITTING, COMMITTED,
ROLLING_BACK and ROLLED_BACK. Each pending intent is durable before publication;
installed identities are recorded after exact verification. Unknown publication
between rename and journal confirmation remains pending/uncertain and refuses
automatic adoption or rollback. Evidence remains available for independent review.

The synthetic core installs dependencies first, then shared compatibility/CLI,
and incident engine LAST. Individual publication is atomic, not the entire set.
New-name publication uses Linux renameat2 NOREPLACE; replacement preserves approved
destination UID/GID/mode. Existing engine 0755 is never overwritten with Git 0644.
Existing target bytes/identity/ancestors are rechecked immediately before replacement.

Separately authorized rollback accepts COMMITTED or a recorded COMMITTING prefix
with no pending uncertainty. It validates all targets and needed backups before
any restoration, processes the proven installed subset in reverse, restores exact
old bytes/UID/GID/modes and removes only proven new targets. Partial rollback or
unknown pending publication stops for review, without automatic continuation.
Restoration creates new filesystem identities; original inode, ctime and mtime
are not claimed restored. Original metadata remains recorded as evidence.

### Consumer coordination: supplied facts and deliberate native block

The following exact commands are OPERATOR_SUPPLIED from PI3 crontab -l, not
inferred from installer templates:

~~~text
*/1 * * * * flock -n /tmp/hioc-incident-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-incident-engine-v2.py
*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py
17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py
~~~

Native preflight checks each occurs exactly once and binds the whole crontab hash.
It does not install crontab or assume every caller participates in those locks.
UNLOCKED_ASSET_OR_CLASSIFICATION_CALLERS=NOT_EXCLUDED.
NativeConsumers.hold deliberately raises CONSUMER_COORDINATION_NOT_ESTABLISHED;
matching hashes, three locks or a declared authorization cannot bypass it.
Neither native commit nor rollback is currently deployable.

Synthetic success/failure/rollback uses an explicitly test-only, externally owned
consumer fence held independently of controller exceptions. This demonstrates
transaction behavior under that stated boundary; it does not supply a PI3 fencing
mechanism, universal caller exclusion or power-loss/process-crash safety evidence.
The independent partial-transaction exclusion prerequisite remains unresolved.
A future native coordinator must establish that boundary before publication can be
enabled; do not replace this gate with an operator boolean or inferred cron absence.

### Validation and remaining delivery prerequisites

Deterministic tests live in tests/test_pe73_pi3_delivery.py. Native Windows
temporary files, file fsync/replace, hard links and AssetLock contention are used.
POSIX owner/mode/ACL/ancestor cases and the external fence are explicitly synthetic;
Linux descriptor traversal, renameat2, directory fsync and native production locks
are not claimed executed. No fixture touches a production root or runs payload.

The matrix covers exact 13 Git identities/order/modes; all five replacement and
eight absence mismatches; release/root/remote pinning; symlink/hard-link, ACL,
owner/mode checks; stale or missing authorization; backup/staging corruption;
every publication position; interruptions before/after durable installation identity;
partial-state refusal; separate rollback and drift refusal; native Windows lock
contention; truthful native consumer refusal; unrelated-file preservation and
no job/network/cron/configuration side effects. Exact final test counts and tested
source identities are recorded below after the final unchanged-code run.

Remaining PI3 prerequisites: fresh exact target/parent/backup/staging metadata and
absence checks, actual native capabilities, verified controller runner provenance,
and a demonstrated complete consumer/exclusion boundary including independent
Asset/classification callers and partial-transaction recovery conditions.
Known cron evidence is retained; no repeat crontab observation is requested just
to rediscover the supplied commands. Revalidation at actual mutation remains mandatory.

Remaining HA prerequisites are unchanged and outside this PI3-only candidate:
actual installed API/version/resource/Dashboard support, supported configuration
and private trust placement, operator/backend ACL and endpoint/certificate facts,
guarded backup/delivery with editing/observations/notifications disabled.
No HA artifact delivery, credential creation or service change occurs here.

Accepted PE-7.1 runtime sources, contract and original tests are unchanged. Existing
evidence/history and the four-file historical fingerprint limitation are preserved.
No full native product regression is repeated; this is deployment-tool synthetic
validation, not PE-7.4 behavior acceptance. No production access or mutation,
deployment/rollback execution, PE-7 activation, staging, commit or push occurs.
Next action: independent repository review of this candidate and its explicit
native coordination gate. PE-7.3 remains OPEN / IN_PROGRESS.


### Final PE-7.3 native synthetic result

Selection: unittest.defaultTestLoader.loadTestsFromName('test_pe73_pi3_delivery').
Final unchanged-code run: 31 run, 31 directly counted passes, zero failures,
zero errors, zero individual skips and zero class-level skips; 42.672 seconds.
Established harness: bundled Windows Python stdin with -B,
sys.path[:0]=['tests','pi4/lib'], UTF-8, HIOC_TEST_SHELL cleared and shell-free PATH
(System32, Windows, WindowsPowerShell/v1.0, Git/cmd). Result counts and pre/post
tool/test hashes are captured directly in temporary
hioc-pe73-delivery-native-result.json, independently of console preservation.
Earlier intermediate 24/24, 30/30 and 31/31 results apply to those earlier tool bytes;
the final source identities below supersede them for this candidate.

- tests/test_pe73_pi3_delivery.py: SHA256 125e12df439e71f0a20a10c8b1e8de93a33d45b258ff6d5b60cbaf8b63004b0d; Git blob d41c5cc86b8845fae615135873cbf91b46e4b9c8.

- tools/hioc-pe73-pi3-delivery.py: SHA256 a51d4a33904ce455a13b02678ee04113fa37fd38ea56b5c4efb8ee20a4d7cebb; Git blob cbe9efd33bc630b1b200b100a68cff8db574551e.

Native live commit and rollback remain deliberately blocked. Synthetic success
is not production consumer-coverage evidence, deployment authorization or PE-7.3 closure.


### PE-7.3 two-defect correction after independent rejection

The original independent disposition remains REJECT for the pre-correction
controller a51d4a33904ce455a13b02678ee04113fa37fd38ea56b5c4efb8ee20a4d7cebb
and tests 125e12df439e71f0a20a10c8b1e8de93a33d45b258ff6d5b60cbaf8b63004b0d.
The 31/31 receipt above is retained for those original bytes. This correction
repairs only the two confirmed internal correctness defects; it is not independent
acceptance, production permission or PE-7.3 closure.

Before controller mutation, three focused regressions reproduced the defects:
3 run, 3 expected failures, 0 errors. Child validation left an acquired descriptor
open. Two malformed journal cases failed to reject ROLLED_BACK without restoration
and COMMITTED containing restoration overrides. These are synthetic failures,
not observed production transactions.

Descriptor ownership is now recorded immediately after every successful open.
All owned descriptors receive exactly one close attempt, in reverse acquisition
order, even after validation/open/body failure. Cleanup continues after close
failure; a primary rejection is preserved and marked cleanup_failed (with a
sanitized note where supported). With no primary failure, cleanup failure is
reported. Close is never retried because its descriptor may already be released;
a failing OS close is not claimed to prove that the descriptor was released.
No no-follow, metadata or ancestry guard was weakened.

Recovery inspection now validates closed bounded journal/snapshot fields, exact
integer/boolean types, authorization syntax and required state relationships,
consumer-observation structure, installed-prefix identities and parent bindings,
and reverse installation-order restoration membership. COMMITTED forbids restored
entries; ROLLED_BACK requires restoration of every recorded installation and
rollback authorization. Restored replacement hashes are bound both to the original
accepted baseline and the actual private backup bytes. New targets require recorded
absence restoration. Duplicate JSON keys, extra entries, conflicting progress and
invalid pending paths are rejected. Pending intent remains uncertain. Valid partial
rollback inspection can establish the exact recorded mixed state; it does not
claim completed rollback, authorize consumers or enable automatic resume.
These structural checks do not authenticate human authorization or invent missing
history; authorization references remain explicit local declarations.

Validation: established bundled native Windows Python stdin harness, -B,
sys.path[:0]=['tests','pi4/lib'], UTF-8, shell-free PATH and HIOC_TEST_SHELL cleared.
Selection: unittest.defaultTestLoader.loadTestsFromName('test_pe73_pi3_delivery').
Final run: 47 run, 47 directly counted passes, 0 failures, 0 errors, 0 skips,
0 class-level skips, 115.355 seconds. All 31 existing tests and 16 new regressions
executed together. Tool/test bytes were unchanged across the run. Exact counts and
source identities are also retained in temporary hioc-pe73-correction-result.json.
No full historical suite was run. New native traversal tests use controlled
mock descriptors; existing Windows temporary-file, replacement, fsync and lock
fixtures remain synthetic evidence, not native Linux or production execution.

- tools/hioc-pe73-pi3-delivery.py: SHA256 3b63d84b0f1641561161fa8d8a353418ccfbf731df35ef947236ffea7686f412.
- tests/test_pe73_pi3_delivery.py: SHA256 ff95bdfd06d55e4f120868e025a161521e551de4d8e93004e99362cd9cc146e7.

Preservation verification: exact 13-file release manifest and installation order
unchanged; accepted PE-7.1 source/contract preserved; all 39 successor identities
and 449 protected identities remain valid under existing raw/canonical-byte rules.
Only the two current documentation identities are refreshed in the existing
successor record; no historical artifact identity is rewritten. Existing evidence
and the four-file historical fingerprint limitation are retained. No unrelated
candidate path is introduced; git diff --check passes.

NativeConsumers and its unconditional commit/rollback refusal are unchanged.
UNLOCKED_ASSET_OR_CLASSIFICATION_CALLERS=NOT_EXCLUDED; three supplied cron locks
remain incomplete coverage. Complete consumer exclusion across partial publication
and controller failure is still NOT_ESTABLISHED. No maintenance coordinator,
cron/systemd change, automatic rollback or override was implemented.

PE73_TWO_DEFECT_CORRECTION=PASS_REPOSITORY_SYNTHETIC.
PE73_PI3_DELIVERY_CANDIDATE=PARTIAL; independent focused recheck is pending.
PE73_COMPLETE=FALSE; production delivery/rollback remain blocked. No PI3/PI5 access,
deployment, migration, monitoring/notification activation, staging, commit or push
was performed. PE-7.4 remains NOT_AUTHORIZED. Next action: focused independent
recheck of these two corrections within the existing candidate.


### PE-7.3 bounded consumer-maintenance implementation with production gates

PE73_CONSUMER_MAINTENANCE_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC.
The corrected pre-extension controller/test pair above received
PE73_PI3_CONTROLLER_FOCUSED_RECHECK=ACCEPT_WITH_EXPLICIT_BLOCKER. That independent
acceptance is retained for its exact scope; this extension still requires bounded
independent review. PE-7.0/7.1/7.2 remain COMPLETE/PASS. PE-7.3 remains IN_PROGRESS,
not COMPLETE/PASS. PE-7.4 remains NOT_AUTHORIZED.

#### Single transaction authority and bounded maintenance progress

The existing delivery journal, under the same pe73-pi3-delivery-v1 transaction,
can now contain one closed optional maintenance member. No parallel transaction
journal, checkpoint, service, scheduler framework or automatic recovery loop is
introduced. Existing journals without that member retain their accepted strict
validation. The only changes to existing controller methods are the optional
maintenance validation hook and maintenance-progress synchronization in _save.
Accepted descriptor cleanup, NativeConsumers, CLI/UID/GID contract, source gate,
13-item manifest, five backups, eight absence expectations, publication order and
separate provenance-bound rollback are unchanged. All 47 existing test methods
and fixtures remain unchanged; 27 maintenance regressions are added.

Maintenance progress is subordinate to the existing installation state:

| Evidence/progress | Recorded phase |
| --- | --- |
| No maintenance member | NOT_ESTABLISHED (inspection only) |
| Preservation intent / verified original scheduler backup | PRESERVATION_UNCERTAIN / SCHEDULER_PRESERVED |
| Exclusion intent / exact excluded scheduler observed | EXCLUSION_UNCERTAIN / LAUNCHES_EXCLUDED |
| Restriction intent / exact conditional fence observed | FENCE_UNCERTAIN / FENCE_ESTABLISHED |
| Drain intent / complete fixture process boundary | DRAIN_UNCERTAIN / CONSUMERS_DRAINED |
| Scheduler, fence and current drain proof rechecked | ESTABLISHED |
| Existing COMMITTING / COMMITTED transaction | INSTALLATION_UNCERTAIN / INSTALLATION_VERIFIED |
| Existing ROLLING_BACK / ROLLED_BACK transaction | ROLLBACK_UNCERTAIN / RESTORATION_VERIFIED |
| New separately authorized drain after context change | REDRAIN_UNCERTAIN, then reverified previous held phase |
| Exact verified runtime plus separate release declaration | RELEASE_AUTHORIZED |
| Scheduler restoration intent / exact original scheduler observed | SCHEDULER_RESTORE_UNCERTAIN / SCHEDULER_RESTORED_FENCED |
| Final access restoration intent / security metadata observed | ACCESS_RELEASE_UNCERTAIN / ACCESS_RESTORED_VERIFIED |

Each effect has a durable prior intent and a separately observed postcondition.
Ordered authorization history, unique references, current journal digest, closed
record fields and transaction/progress relationships are checked. A phase label
alone supplies neither exclusion nor production permission. Inspection separately
reports observed scheduler digest and fence/restoration metadata matches.

#### Scheduler, caller inventory and conditional fence

The complete original crontab is retained as exact private crontab-original bytes
in the same transaction and hash-bound by the journal. Account UID/GID and available
interface metadata are retained and compared. Unknown cron-spool metadata is not
invented. No cron spool path or scheduler command is implemented by the new seam.
Only exact explicitly approved job lines are excluded; all other bytes, including
comments, blank lines, history and unrelated jobs, are preserved. A complete explicit
classification of active entries is required; missing, duplicate or inconsistent
inventory stops. All three previously supplied cron entries remain OPERATOR_SUPPLIED
facts. Extra PE-4/PE-5/history commands in tests are /fixture examples only, never
claimed actual production commands or authorization to pause those jobs.

The synthetic scheduler interface checks expected current bytes and reobserves the
result. This fixture check is not proof of a native crontab compare-and-swap API.
Native qualification still requires an exclusive scheduler-editor boundary before
mutation, actual scheduler inventory and separately approved collateral pauses.
There are no catch-up executions or changes to freshness/snapshot-age policy.

The exact conditional fence target is /home/jazofv1/hioc/pi4/lib/hioc; proposed
restricted mode is 0000. Original device/inode, directory type, numeric UID/GID,
mode and ACL disposition are bound. Exact original security metadata, not original
ctime, is checked on release. Mode 0000 is not claimed universally effective:
the owner can change permissions, privileged callers can bypass ordinary access,
open descriptors remain usable and already-imported modules can continue executing.
Processes under other identities and other package users must be covered explicitly.
The native ancestor policy is not weakened to accommodate an unqualified fence.

Windows-only MaintenanceConsumers and injected synthetic operations model this
conditional mechanism. Current process-boundary proof includes enumerated identities,
drained readers/cached modules/open descriptors, privileged caller exclusion,
permission-editor exclusion, alternate-launcher exclusion and persistence qualification,
all explicitly SYNTHETIC_ONLY. An observation session change invalidates the old
proof; new drain qualification requires a fresh authorization. An interrupted
requalification remains REDRAIN_UNCERTAIN rather than an established boundary.
This models restart reconstruction from the retained journal and retained fixture
effects; it does not execute an OS reboot or prove native process exclusion.

NativeFenceInterface exposes only restrict(reference, binding) and restore(reference,
binding) for the fixed target. Both unconditionally reject with
NATIVE_FENCE_NOT_QUALIFIED. No arbitrary path, command, shell, sudo, root execution,
permission mutation, credential or privileged service is supplied. Maintenance
integration rejects non-Windows use and the NativeConsumers provider. No matching
receipt, environment setting or new CLI flag enables native publication.

#### Installation, rollback, release and uncertainty

MaintenanceConsumers rechecks actual fixture scheduler, fence and current process
proof before the existing controller can publish or roll back. Nothing releases
the fence on context exit, exceptions, SSH-loss modeling, interruption or successful
installation. The journal records effects; persistent fixture state supplies the
simulated exclusion. Recorded partial installations and unknown pending publications
remain distinct; neither qualifies for consumer release.

After complete installed-set verification or complete separately authorized rollback,
a fresh release declaration is bound to exact runtime evidence. Scheduler restoration
is then verified while access remains restricted. Before final access restoration,
the original scheduler, held fence, current process proof and exact runtime binding
are rechecked. Final restoration requires another fresh reference/binding. Stale,
reused, duplicate or premature requests fail. No automatic resume, automatic rollback
or retry is introduced. Explicit redrain after interrupted requalification is distinct
from automatic transaction recovery. Other uncertain effect outcomes stop for review.

If final access restoration takes effect but its confirmation fails, the journal
remains ACCESS_RELEASE_UNCERTAIN; inspection can report matching current metadata
without claiming verified release. The runtime had already been fully verified and
release separately declared before that effect. No subsequent automatic file mutation
or rollback is allowed. A failed scheduler restoration leaves access fenced.

#### Validation evidence and limits

The complete test module was run with the established bundled native Windows Python
stdin harness, -B, sys.path[:0]=['tests','pi4/lib'], UTF-8, shell-free PATH and
HIOC_TEST_SHELL cleared. Selection:
unittest.defaultTestLoader.loadTestsFromName('test_pe73_pi3_delivery').
Final unchanged-source run: 74 run, 74 passed, 0 failures, 0 errors, 0 skips, 0 class-level skips.
Unittest elapsed: 189.734 seconds; receipt harness elapsed including selection: 191.25 seconds.
Directly counted totals and pre/post source hashes are retained in temporary
hioc-pe73-maintenance-result.json. The original 47 tests and all 27 new tests ran
together. Both 13-position matrices cover interruption after recorded installation
and after publication before confirmation; neither produces automatic release.
Other cases cover scheduler preservation/exclusion/concurrency, restriction uncertainty,
drain and independent-caller failures, ordered authorization history, restart/redrain,
interrupted rollback, release authorization and exact restoration, drift/tampering,
privileged-interface refusal and absence of commands/network/native fence changes.
The existing Windows AssetLock may set mode 0600 on its exact isolated fixture lock;
the instrumentation permits only that expected lock operation, not package chmod.

Development evidence is retained: an initial run stopped at 57 tests (56 passes,
1 failure plus 1 teardown error) because an overbroad chmod mock blocked AssetLock's
legitimate fixture setup. The mock was narrowed without changing AssetLock or its
original tests. A later run stopped at 60 tests (59 passes, 1 failure, no errors)
on a Windows-backslash rendering of the new fixed POSIX target; the contract target
was made an explicit POSIX literal. Focused checks passed after correction, including
15 tests covering the remaining native-interface/recovery and descriptor paths.
The final full-module result above supersedes those intermediate candidate runs.
No full historical HIOC suite was run.

- tools/hioc-pe73-pi3-delivery.py: SHA256 ac55aa8baa5c0ee26c53cb54b020fd4ca6ec79201b769795781a31868389668e.
- tests/test_pe73_pi3_delivery.py: SHA256 24f2616e4a0076297724cc75c59e4633a487e2cf112b2d714aedcae9809a080e.

These results prove synthetic state-machine behavior only. They do not prove Linux
permission semantics, cron atomicity/durability, privilege security, reboot persistence,
actual caller exclusion or production isolation. Every maintenance inspection marks
production_qualified=false. NativeConsumers.hold and assert_active remain unchanged
and unconditional; native commit and rollback remain blocked.

Required native prerequisites remain: verified directory/ancestor metadata and native
capabilities, a separately reviewed/authorized least-privilege implementation, complete
actual launcher/identity/process coverage, current scheduler/editor exclusion, safe
reader draining, owner/privileged access control, persistence qualification, explicit
PE-4/PE-5/package-consumer pause approval and separately authorized final release.
No Pi-hole DNS/DHCP, Unbound, NUT or unrelated service/schedule change is authorized.

Final static preservation: accepted PE-7.1 source/contract, exact 13 identities,
all 39 successor identities and 449 protected identities verified. Only current
Master Plan and existing implementation-evidence identities are refreshed in the
existing successor record. Historical evidence, limitations and production provenance
labels are preserved. git diff --check passes; no new repository path is introduced.
No staging, commit, push, PI3/PI5 access, production permissions/cron/service changes,
deployment/rollback execution, credentials, migration, monitoring or notification
activation occurred. PE-7.3 remains IN_PROGRESS with native delivery prohibited;
PE-7.4 remains NOT_AUTHORIZED. Next action: bounded independent repository review
of this maintenance extension and its preserved native gates.


### PE-7.3 fresh-provider recovery attachment correction

PE73_MAINTENANCE_INDEPENDENT_REVIEW=REJECT is preserved for controller
ac55aa8baa5c0ee26c53cb54b020fd4ca6ec79201b769795781a31868389668e and tests
24f2616e4a0076297724cc75c59e4633a487e2cf112b2d714aedcae9809a080e.
The confirmed defect was fresh construction treating an already-reduced maintenance
scheduler as the original scheduler. The previous restart test reused its provider
and did not establish recovery after losing that provider's memory. The original
74/74 result above remains historical evidence for its exact tested bytes.

Before controller mutation, OriginalRecoveryRegression instantiated a fresh provider
against the reduced scheduler. The single regression produced the exact expected
MAINTENANCE_JOB_INVENTORY error (1 run, 1 expected error, 0 assertion failures).
Its output is retained in temporary hioc-pe73-recovery/pre-correction-reproduction.txt.
This is a Windows synthetic reproduction, not a production observation.

#### Strict initial path versus explicit recovery attachment

The original constructor still reads the actual scheduler and enforces the exact
original inventory using unchanged maintenance_cron rules. It is not relaxed to
accept a reduced scheduler. A newly created initial maintenance context must bind
before a transaction exists. Once a transaction exists, a new context must use the
explicit recovery attachment even if the original scheduler has already been
restored. This prevents the initial path from inheriting a former process proof.

MaintenanceConsumers.attach(fs, source, ops, reference, binding) is a separate
Windows-only factory. It returns a new controller with a new provider; no previous
provider, controller, cached original plan or process-proof object is required.
It validates the existing strict journal and exact supplied journal digest, source
manifest, version/release, maintenance scope, retained original scheduler bytes,
original consumer binding, approved exclusion inventory and scheduler metadata.
It observes current scheduler bytes, fence metadata and all 13 runtime targets.
Unknown historical transactions, missing/corrupt backups, conflicting identities,
unsupported versions, duplicate fields, changed job sets and runtime drift stop.

Current scheduler and fence evidence must match the exact phase-permitted states.
An interrupted scheduler exclusion/restoration can observe either exact legitimate
configuration, without advancing its uncertain phase. An interrupted restriction
or final access release similarly retains uncertainty after observing either exact
legitimate fence state. A pending publication/restoration may have its exact
recorded before-state or approved after-content; attachment never adopts that
content into installed/restored identities or clears pending intent. All other
runtime bytes and ancestry must match their existing recorded identities.

Attachment never modifies scheduler, permissions, runtime files or progress phase.
Its only write is a fresh ATTACH authorization in the existing private transaction
journal, serialized under the existing deployment mutex. Duplicate/stale bindings
and reused references are rejected. The latest ATTACH event invalidates older
provider contexts durably. Every fresh provider requires new process qualification,
even when a backend repeats an old session token. Old process observations remain
historical evidence, not renewed execution authority.

Authorization-history validation admits ATTACH as a read/requalification event
without advancing the strict effect sequence. REDRAIN requires explicit fresh
permission and retains an uncertain intent until its new evidence is verified.
Requalification can preserve an already verified release/scheduler-restoration
phase; it does not create a new release declaration or clear unknown effects.
Completed ACCESS_RESTORED_VERIFIED transactions reject attachment for new maintenance.
A COMMITTED runtime still under maintenance can be inspected/attached, but cannot
release or roll back merely because it is COMMITTED: fresh drain evidence and the
existing separate operation authorizations remain required.

#### Regression evidence and preservation

New tests construct fresh provider/controller/backend objects from the on-disk
transaction and serialized modeled external scheduler/fence effects. They recover
original fixture restore metadata only after the persisted originals are validated.
The old provider/controller are discarded in these reconstruction tests. A separate
negative test deliberately retains an older context and verifies that the latest
recorded attachment makes it unusable.

The 30 new regressions cover strict initial construction; reduced scheduler
reconstruction; prepared maintenance before/after exclusion; same-token stale proof;
recorded partial publication; unconfirmed publication; interrupted rollback; committed
held state; release-authorized and scheduler-restored attachment; missing/corrupt/
mismatched backups; wrong job sets/release/version; duplicate/conflicting fields;
unexpected scheduler, fence type/identity or artifact drift; completed and unrelated
transactions; duplicate/stale authorization; uncertain scheduler and access outcomes;
initial-context misuse; and native attachment refusal.

An intermediate combined run passed 103/103. An additional initial-path regression
then demonstrated that a new initial context was not refused against an existing
transaction after scheduler restoration (1 expected assertion failure). The initial
context guard was added, and that test plus valid fresh preparation/recovery paths
passed 3/3 before the final combined run. These refinements remain within the single
initial-preparation versus recovery-attachment correction. Prior intermediate
results are not presented as final-source validation.

Final selection: unittest.defaultTestLoader.loadTestsFromName('test_pe73_pi3_delivery').
The established bundled native Windows stdin harness used -B,
sys.path[:0]=['tests','pi4/lib'], UTF-8, shell-free PATH and HIOC_TEST_SHELL cleared.
Final result: 104 run, 104 passed, 0 failures, 0 errors, 0 skips, 0 class-level skips.
Unittest elapsed: 244.898 seconds; receipt harness elapsed: 246.359 seconds.
All 74 existing tests and fixtures remain unchanged; all 30 new tests ran with them.
Tool/test hashes were unchanged across the final run. Exact directly counted totals
and source hashes are retained in temporary hioc-pe73-recovery-result.json.
No full historical HIOC suite was repeated.

- tools/hioc-pe73-pi3-delivery.py: SHA256 0589cf6363626d14ab9abe08c001ddef634b243326513b27de43a7b93aa4f95f.
- tests/test_pe73_pi3_delivery.py: SHA256 4fef3799a3bae5733056fa30b3423bca656026103a6ce02e443e14ac639ce281.

The main controller journal validator, source gate, 13-artifact manifest, five original
replacement identities, eight absence expectations, dependency/engine-last ordering,
exact backup/rollback code, descriptor lifecycle and unconditional NativeConsumers/
NativeFenceInterface refusal remain unchanged. Existing scheduler-preservation rules
and fence limitations are retained. All 39 successor identities and 449 protected
identities are valid; only the two current documentation identities are refreshed
in the existing successor record. Historical accepted evidence and the four-file
fingerprint limitation are preserved. git diff --check passes; no new repository
path is introduced.

PE73_RECOVERY_ATTACHMENT_CORRECTION=PASS_REPOSITORY_SYNTHETIC, not independent
acceptance or production qualification. No native backend, CLI switch, environment
bypass, privileged execution or receipt-as-permission path is added. Synthetic tests
do not establish Linux permission enforcement, process exclusion, cron atomicity or
reboot persistence. All existing native qualifications, caller/identity coverage,
privilege/editor boundaries and explicit production/release authorizations remain
required. No PI3/PI5 access, production cron/permissions/service changes, deployment,
rollback, credentials, migration, monitoring or notifications occurred. No staging,
commit or push. PE-7.3 remains IN_PROGRESS; PE-7.4 remains NOT_AUTHORIZED.
Next action: focused independent recheck of this recovery-attachment correction.


### PE-7.3 bounded native qualification preparation

Classification: CURRENT preparation, not qualification or production permission.
PE73_RECOVERY_FOCUSED_RECHECK=ACCEPT_WITH_NATIVE_GATES is the separately supplied
independent decision for controller SHA256
0589cf6363626d14ab9abe08c001ddef634b243326513b27de43a7b93aa4f95f and tests SHA256
4fef3799a3bae5733056fa30b3423bca656026103a6ce02e443e14ac639ce281.
Earlier independent REJECT and then-pending correction narratives remain historical.
PE73_NATIVE_QUALIFICATION_PREPARATION=PASS; NATIVE_QUALIFICATION=NOT_PERFORMED.
PE-7.2 COMPLETE/PASS; PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
No implementation, native enablement, staging, commit or push is authorized.

#### Authority and established evidence reused

Authority: [PE-7 contract section 13](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md#13-bounded-checkpoint-sequence-and-implementation-scope),
current Master Plan and preserved guarded-delivery/maintenance evidence above.
Accepted artifact release remains 51398bab4e2293b578b2cdac2d0740c3738cab2f.
The 13-file manifest, five replacement identities/modes, eight absence expectations,
dependency-first/incident-last ordering and 104/104 Windows receipt are preserved.
Those are repository/synthetic facts, not native qualification observations.

Reused OPERATOR_SUPPLIED facts: nutandpihole (PI3 NUT&PIHOLE), LAN 192.168.100.252;
release-source /home/jazofv1/hioc-release-source; non-Git runtime /home/jazofv1/hioc;
UID/GID 1000:1000; five supplied replacement identities and eight absent new targets.
Actual supplied jobs:

- */30 * * * * flock -n /tmp/hioc-inventory-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py
- 17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py
- */1 * * * * flock -n /tmp/hioc-incident-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-incident-engine-v2.py

Existing history, PE-4, PE-5 and monitoring schedules remain acknowledged. Fixture
examples are not substituted for their actual commands. These three locks do not
exclude manual Asset/classification, service, privileged or cached-module callers.
Do not ask to rediscover established facts. Immediately before any future separately
authorized production mutation, recheck only the mutable bindings that can become
stale: target/ancestor identities, scheduler/editor boundary, actual affected callers,
backup readiness and exact operation authorization. Qualification is not that gate.

Precedents govern semantics, not executable reuse:

- tools/hioc-pe4-ha-association-deploy.py: transaction_state validates secured intent,
  backups and exact committed marker. Durable historical directories alone are not
  conflicts; never delete or reinterpret historical journals.
- [PE-5 persistence/recovery](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#persistence-and-explicit-recovery):
  bounded no-follow reads, file/parent fsync, confirmed versus pending effects,
  explicit recovery and no automatic adoption. Visibility is not durability.
  Its deployment-readiness section establishes CPython 3.10 as the language floor.
- release/upgrade.sh broadly copies and calls install_pi4.sh; release/rollback.sh
  similarly copies and calls the installer. Neither is a bounded PE-7.3 qualifier.
  Do not run these, an installer, an HIOC entrypoint or the controller here.

#### Action 1: only immediate operator action, read-only capability inventory

Machine: PI3 NUT&PIHOLE; user: jazofv1. Run this complete block from any directory.
No SSH command is supplied; Codex does not connect. No sudo/root invocation.
Return its entire sanitized JSON and exit status, then STOP. Do not chain stages.

This does not import HIOC, read credentials/private Asset/HA content, execute engines,
call fsync/rename/flock/chmod, create files/locks, inspect process arguments/environment,
change cron or access network. Crontab bytes remain private; only hashes/counts leave
the command. Read access can update filesystem atime; no application write is requested.
A capability inventory PASS is neither native behavioral qualification nor permission.

```sh
/usr/bin/python3 -I -S -B - <<'PY'
import ctypes
import datetime
import errno
import hashlib
import json
import os
import pathlib
import platform
import shutil
import socket
import stat
import subprocess
import sys

r = {"kind": "READ_ONLY_CAPABILITY_INVENTORY", "target": "PI3 NUT&PIHOLE",
     "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
     "production_authorization": False, "native_qualification_complete": False,
     "writes_requested": False, "locks_created": False, "engines_executed": False}
issues = []
try:
    if socket.gethostname() != "nutandpihole" or platform.system() != "Linux":
        raise ValueError("TARGET_MISMATCH")
    if (os.getuid(), os.geteuid(), os.getgid(), os.getegid()) != (1000, 1000, 1000, 1000):
        raise ValueError("IDENTITY_MISMATCH")
    r["environment"] = {"kernel": platform.release(), "machine": platform.machine(),
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "interpreter": sys.executable, "uid": os.getuid(), "gid": os.getgid()}
    if sys.version_info < (3, 10) or platform.python_implementation() != "CPython":
        issues.append("REPOSITORY_PYTHON_FLOOR_NOT_MET")
    r["flags"] = {n: hasattr(os, n) for n in
        ("O_DIRECTORY", "O_NOFOLLOW", "O_CLOEXEC", "O_NONBLOCK", "O_EXCL")}
    r["functions"] = {n: hasattr(os, n) for n in
        ("replace", "fsync", "fchmod", "getxattr", "stat", "unlink")}
    r["dir_fd"] = {n: getattr(os, n) in os.supports_dir_fd for n in
        ("open", "stat", "mkdir", "rename", "unlink")}
    import fcntl
    r["flock_symbol"] = hasattr(fcntl, "flock")
    r["renameat2_symbol"] = hasattr(ctypes.CDLL(None, use_errno=True), "renameat2")
    if not all(r["flags"].values()) or not all(r["functions"].values()) or not all(r["dir_fd"].values()) or not r["flock_symbol"] or not r["renameat2_symbol"]:
        issues.append("REQUIRED_PRIMITIVE_NOT_EXPOSED")
    observed = []
    fd = None
    try:
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for part in (None, "home", "jazofv1", "hioc", "pi4", "lib", "hioc"):
            if part is not None:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
                old = fd
                fd = child
                os.close(old)
            s = os.fstat(fd)
            entry = {"component": part or "/", "device": s.st_dev, "inode": s.st_ino,
                "uid": s.st_uid, "gid": s.st_gid, "mode": format(stat.S_IMODE(s.st_mode), "04o"),
                "type": "DIRECTORY" if stat.S_ISDIR(s.st_mode) else "UNSAFE", "acl": {}}
            if not stat.S_ISDIR(s.st_mode) or s.st_uid not in (0, 1000) or stat.S_IMODE(s.st_mode) & 0o7022:
                issues.append("ANCESTOR_POLICY_MISMATCH")
            for name in ("system.posix_acl_access", "system.posix_acl_default"):
                try:
                    os.getxattr(fd, name)
                except OSError as e:
                    entry["acl"][name] = "ABSENT" if e.errno == errno.ENODATA else "UNKNOWN"
                else:
                    entry["acl"][name] = "PRESENT"
                if entry["acl"][name] != "ABSENT":
                    issues.append("ACL_POLICY_NOT_ESTABLISHED")
            observed.append(entry)
        if observed[-1]["uid"] != 1000 or observed[-1]["gid"] != 1000:
            issues.append("FENCE_IDENTITY_MISMATCH")
    finally:
        if fd is not None:
            os.close(fd)
    r["fixed_path_observations"] = observed
    known = (
        b"*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py",
        b"17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py",
        b"*/1 * * * * flock -n /tmp/hioc-incident-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-incident-engine-v2.py")
    proc = subprocess.Popen(["/usr/bin/crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"PATH": "/usr/bin:/bin", "HOME": "/home/jazofv1", "LANG": "C", "LC_ALL": "C"})
    try:
        raw, err = proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        raise ValueError("CRONTAB_READ_TIMEOUT") from None
    if proc.returncode != 0 or len(raw) > 65536 or len(err) > 65536:
        raise ValueError("CRONTAB_READ_NOT_ESTABLISHED")
    counts = [raw.splitlines().count(line) for line in known]
    r["scheduler"] = {"inspection": "/usr/bin/crontab -l", "returncode": proc.returncode,
        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "known_entry_counts": counts,
        "implementation_version": "NOT_ESTABLISHED", "exclusive_editor_boundary": "NOT_ESTABLISHED",
        "cron_python_resolution": "NOT_ESTABLISHED"}
    if counts != [1, 1, 1]:
        issues.append("KNOWN_SCHEDULER_ENTRY_CHANGED_REVIEW_REQUIRED")
    pids = [p for p in pathlib.Path("/proc").iterdir() if p.name.isdigit()]
    if len(pids) > 8192:
        raise ValueError("PROCESS_ENUMERATION_LIMIT")
    readable = vanished = unresolved = 0
    for p in pids:
        try:
            p.stat()
            (p / "exe").readlink()
            readable += 1
        except FileNotFoundError:
            vanished += 1
        except OSError:
            unresolved += 1
    r["process_discovery"] = {"numeric_entries": len(pids), "exe_links_readable": readable,
        "vanished": vanished, "unresolved": unresolved, "complete_caller_coverage": False,
        "cached_modules_or_open_readers_excluded": False}
    r["runtime_env_python_on_fixed_search_path"] = shutil.which("python3", path="/usr/bin:/bin")
    r["RESULT"] = "PASS_READ_ONLY_CAPABILITY_INVENTORY" if not issues else "INSUFFICIENT_EVIDENCE"
except Exception as e:
    r["RESULT"] = "INSUFFICIENT_EVIDENCE"
    r["failure_type"] = type(e).__name__
    r["failure_code"] = str(e) if type(e) is ValueError and str(e) in {"TARGET_MISMATCH", "IDENTITY_MISMATCH", "CRONTAB_READ_TIMEOUT", "CRONTAB_READ_NOT_ESTABLISHED", "PROCESS_ENUMERATION_LIMIT"} else "CAPABILITY_OR_READ_NOT_ESTABLISHED"
r["issues"] = sorted(set(issues))
r["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
r["STOP_REQUIRED"] = True
print(json.dumps(r, sort_keys=True, separators=(",", ":")))
raise SystemExit(0 if r["RESULT"] == "PASS_READ_ONLY_CAPABILITY_INVENTORY" else 1)
PY
```

Action 1 output is READ_ONLY/OPERATOR_SUPPLIED when returned by the operator, not
Codex-observed production evidence. It deliberately does not output PIDs, executable
paths, scheduler contents/errors, private exception text or ACL values. The known
three-line counts are not a complete active-job inventory or pause authorization.
Directory observations are sequential, not one atomic snapshot or a future commit
binding. This command buffers expected small crontab output before its size check;
it does not claim a streaming memory bound against a compromised executable.
A process inspection gap is unavailable evidence, not proof of a dangerous process.

#### Action 2: independent capability assessment, then separate isolated authorization

Stop and review Action 1 first. No automatic next command is supplied or authorized.
All actual native results are currently UNKNOWN/NOT_PERFORMED. A missing required
capability or a demonstrated invariant violation is FAIL for that operation; missing
or ambiguous observation is INSUFFICIENT_EVIDENCE. PASS applies only to the exact
observed/tested operation. Required unresolved rows block the dependent native work.

Every row below requires: Q identifier; UTC interval; machine/kernel/architecture;
interpreter path/version; UID/GID; device and object identity; exact operation;
expected invariant; actual result; source class READ_ONLY, ISOLATED_NATIVE or
OPERATOR_SUPPLIED_PRODUCTION; limitations; PASS/FAIL/INSUFFICIENT_EVIDENCE.
Never populate actual values from expected configuration.

| Item | Minimum evidence / tested operation | Boundary and blocking result |
| --- | --- | --- |
| Q01 Linux/Python | Action 1 Linux, CPython >=3.10, architecture/UID/GID; later same-interpreter behavior. | Unsupported floor FAIL; fixed /usr/bin/python3 does not prove cron interpreter selection. |
| Q02 primitives | Flags/functions and isolated exclusive create, fd-relative operations, fchmod, flock. | Symbol presence alone insufficient; unsupported behavior blocks relevant write. |
| Q03 no-follow/descriptors | Anchored directory opens; isolated symlink ELOOP refusal, parent drift rejection and exact-once cleanup with injected failure. | No symlink following or descriptor leak; prior Windows cleanup tests are distinct evidence. |
| Q04 atomic/no-replace | Isolated replace plus concurrent reader sees whole old/new bytes; renameat2 RENAME_NOREPLACE collision EEXIST preserves destination then success on absent target. | Wrong overwrite or mixed bytes FAIL; ordinary rename is not no-replace. |
| Q05 fsync | Isolated file flush/fsync, parent fsync, injected pre/post-sync failures. | Unsupported sync FAIL; successful calls do not prove power-loss durability. |
| Q06 owner/modes | Native ancestor metadata; isolated 1000:1000, private0700/0600, mode0000 new-open denial, owner restoration, already-open fd surviving. | These demonstrate limitations, not universal exclusion; wrong owner/mode FAIL. |
| Q07 ACL | Exact getxattr(fd, access/default) ENODATA versus present/error. | NativeFS rejects ACLs. Present, unsupported or unreadable blocks use; no ACL install/change here. |
| Q08 cron | crontab -l hash/counts; installed binary/package implementation identity, supported interface; complete active-line classification and exclusive editor boundary. | No assumed distribution/spool/CAS. Unknown implementation/editor exclusion blocks mutation. |
| Q09 discovery | /proc visibility; later exact PID+start time+identity/launcher evidence covering independently invoked callers. | Enumeration is not drain; unreadable/unidentified potential callers block proof. |
| Q10 runtime compatibility | Actual interpreter resolution of env-python jobs/manual launchers; accepted artifacts/dependencies syntax and imports in isolated environment. | Fixed search path is not actual cron PATH. No production HIOC imports; unresolved compatibility blocks delivery. |
| Q11 fixed fence | Target/ancestor device/inode/type/UID/GID/mode/ACL and all affected consumers/access identities. | Mode0000 alone insufficient: owner, privilege, open fds, cached modules and alternate paths require coverage. |
| Q12 privilege | Separately reviewed fixed-resource bounded operation and isolated tests; UID1000 delivery contract preserved. | Root-running controller violates TARGET_IDENTITY; UID1000 cannot traverse closed package. No qualified boundary resolves this yet. Blocks dependent production work. |
| Q13 drain/exclusion | Fresh complete manual/service/cron/identity/editor inventory including Asset/classification, PE-4/5/history/monitoring; collateral-pause authorization and persistence evidence. | Existing three locks insufficient; unknown callers or bypasses = INSUFFICIENT_EVIDENCE, no release/install. |
| Q14 termination/recovery | Isolated actual-controller kill at intent/effect/confirmation; new process/provider, retained scheduler backup, observed phase-specific scheduler/fence/artifacts, fresh auth/drain. | Stale proof, label-only adoption, automatic rollback/release FAIL. No qualified native maintenance implementation currently exists. |
| Q15 partial/rollback | Independent secured journal/backups/stages and13 targets; installed-prefix, reverse-restored-prefix, pending uncertainty with isolated failure at boundaries. | Five backups/eight absences/order preserved; missing/corrupt/unconfirmed refuses; release needs separately verified final runtime and fresh authorization. |

The cron implementation/version and actual cron PATH must be observed from installed
package metadata and the actual launch environment before a scheduler/interpreter
mutation gate; neither is invented from installer templates or a default OS assumption.
This does not request another discovery of previously established cron lines.

#### Action 3: isolated behavioral qualification specification, independently gated

NOT AUTHORIZED by this preparation. After Action 1 review, a separate authorization
must approve an exact reviewed fixture runner/identity and effects before execution.
There is deliberately no executable mutation command while Q12 feasibility and the
native runner remain unresolved. The following is the complete allowed test boundary,
not permission to patch the Windows-only seam into a native production backend.

Location: one new unpredictable /home/jazofv1/.hioc-pe73-native-<random> directory,
UID/GID1000:1000 mode0700, outside production package, runtime state/backups and
release-source. Verify no-follow ancestors and same filesystem/device; matching
st_dev alone does not prove equal mount options/storage guarantees. Never use /tmp
for claims about a different production filesystem or write experimental production
package files. Runner must bind its created directory device/inode and exact paths.

Allowed mutations only: private0600 synthetic files and journals; fixed child
fixture directories; synthetic module bytes (not production modules); scratch-only
mode0000/restore; scratch symlink/hardlink rejection fixtures; exclusive temp/create,
replace/no-replace, fsync and scratch flock; owned child test processes and termination
of those exact child PIDs with start-time binding. No production processes/signals,
root, sudo, mounts, reboots, power cuts, cron, services, ACL configuration or network.
No HIOC engines, HA, credentials, Asset metadata or producer execution.

Sequential experiments, each separate receipt and stop on FAIL/unknown:

1. Secure descriptor traversal/no-follow, exclusive create, owned0700/0600 files,
   exact-once descriptor cleanup after validation/open/close failures. No test closes
   an unrelated process descriptor or retries a potentially released descriptor.
2. Same-parent replace with concurrent bounded reader; RENAME_NOREPLACE collision
   refusal and successful new target; file/parent fsync and injected failures.
   Distinguish visible content from confirmed durability, never infer power-loss safety.
3. Scratch-only DAC behavior: mode0000 denies a new ordinary open; owner can restore;
   an already opened file can still be read and loaded synthetic module remains cached.
   Privileged bypass is an untested limitation, never silently waived or root-tested.
4. Simulated complete original scheduler bytes and backup (no crontab installation):
   exact exclusion/preservation, editor conflict, pending intents and release ordering.
   This cannot establish native cron atomicity or real editor exclusion.
5. Once a separately reviewed native-access boundary exists: exact accepted-controller
   harness, kill only created child at every intent/effect/confirmation boundary; fresh
   provider reconstructs from retained journal/backup plus actual scratch effects.
   Preserve pending/unknown writes and failed restoration; never automatically retry,
   adopt, restore cron, remove fence or release. A child kill is not an OS reboot.
6. Independent read-only scratch inspection verifies exact installed/restored prefixes,
   drift rejection, malformed/duplicate/stale authorizations, completed historical
   versus interrupted transaction, full rollback and separate authorized release.

Cleanup/rollback: no production rollback exists in this test. Record primary outcome
and cleanup separately. Restore only the created scratch directory's original0700
through its pinned descriptor; validate identity and complete created-path allowlist,
then unlink only owned fixture leaves and remove only empty created child/root dirs.
No recursive deletion, wildcard/prefix cleanup or traversal of an unexpected link.
On unknown identity/content or interrupted cleanup, retain private fixture, receipt,
exact device/inode/basename and STOP. A later read-only inspection and separate exact
cleanup authorization are required. Do not rerun over retained unknown state.
Cleanup failure cannot hide a primary failure or produce PASS.

Native crash/persistence and real editor/caller coverage remain required even after
primitive tests pass. An isolated fixture does not prove production-wide exclusion.
The actual native-maintenance runner is not implemented and no unqualified command
is offered. This limitation blocks dependent production work, not Action 1.

#### Privilege feasibility, drain and separately authorized later gates

Mode0000 on /home/jazofv1/hioc/pi4/lib/hioc blocks ordinary new traversal, including
NativeFS.directory in this UID1000 controller. Metadata checks can accept mode zero,
but OS permissions still deny the open. Owner can chmod back; root/capabilities can
bypass DAC; cached modules and existing file descriptors remain usable. Other HIOC
consumers share this package. Pausing them may affect incidents, inventory, platform,
PE-4/5, history and monitoring; Pi-hole, Unbound and NUT remain outside scope.
Pauses require explicit bounded collateral/failure disposition, no catch-up or change
to snapshot-age/freshness policy. No pause is authorized here.

Running the controller as root violates main's TARGET_IDENTITY and1000-owned file/
transaction contract. Preopening a directory fd does not establish safe access:
new relative child lookup still requires permissions, and already-open access is
itself a fence limitation. Restrict/restore alone cannot solve this write-access gap.
Existing NativeConsumers and NativeFenceInterface refusals stay unconditional.
No receipt, journal label, CLI flag or environment setting enables native operations.

Minimum separate privilege review: exact fixed target and pinned identity; bounded
restrict/restore transitions; original security metadata/ACL disposition; authenticated
fresh transaction/digest/reference; editor/owner/privileged caller exclusion; finite
invocation lifetime; sanitized independent evidence; failure/crash behavior; preserved
UID1000 artifact ownership. No arbitrary path/command/chown, privilege inheritance
into controller, permanent service or JSON-as-permission. No implementation, sudoers
entry, root command or production enablement is supplied. The design must first
resolve authorized delivery access versus effective exclusion; otherwise STOP.

Process/drain proof must bind actual identities, PIDs+start times, launchers, manual
and service callers, readers, imported modules, open descriptors, privileged actors,
permission/scheduler editors, alternate package paths and persistence. It must be
fresh at every protected operation and invalid after restart/new attachment. Merely
finding no matching /proc entries or holding three cron locks is insufficient.
Unreadable or unknown possible consumers prevent qualification; do not print private
arguments/environment or claim universal coverage from this inventory.

Later production maintenance, artifact installation, recovery and consumer release
are distinct explicit authorizations and evidence gates, never one executable action.
Recovery inspects durable journal/backup and current scheduler/fence/runtime, not old
process memory. COMMITTED-held is not completed release; unknown pending effects,
partial rollback or stale drain forbid release. Restore original scheduler only with
exact backup/editor exclusion while fenced, then separately authorize access release
following verified installed or restored runtime. No auto resume/rollback/release.
A reboot/power-loss guarantee cannot be inferred from SIGKILL or successful fsync.

#### Local preparation validation and stop

Only this existing evidence document, current Master Plan and the directly necessary
two-document identity entries in the existing successor record change. The accepted
controller/tests, contract and runtime artifacts remain byte-identical. No new file,
phase, qualification result or privileged backend is created. Static local validation
checks command syntax and read-only call surface without executing Linux qualification.
Existing104/104 evidence still binds unchanged code; no implementation tests or full
historical suite are rerun. All39 successor and449 protected identities remain valid.

Preparation PASS is a complete bounded evidence/test specification, not native readiness:
Q01-Q15 native results remain UNKNOWN/NOT_PERFORMED and Q12 remains a concrete blocker.
No PI3/PI5 access, production cron/permission/service change, delivery, HA/MQTT/credential
access, migration, activation, staging, commit or push occurs. Exactly one next operator
action: run ONLY Action 1 and return its complete sanitized receipt and exit status.


### PE-7.3 Native Qualification Action 1 recorded and next isolated action

Classification: CURRENT. PE73_NATIVE_ACTION1=PASS_OPERATOR_SUPPLIED.
NATIVE_QUALIFICATION=INCOMPLETE; NATIVE_MAINTENANCE_QUALIFICATION=NOT_ESTABLISHED.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. Native refusal gates are unchanged.
This supersedes the preparation-time UNKNOWN/NOT_PERFORMED and next-Action-1 statements
above only for the observations actually supplied here; those narratives are retained.

#### Actual Action 1 evidence and limits

Evidence source: OPERATOR_SUPPLIED summary in the current user instruction, not a
Codex PI3 observation and not a newly received complete original JSON receipt.
No full-receipt digest, observation interval, per-ancestor device/inode/ACL details,
exact symbol booleans or interpreter binary identity were separately supplied.
Do not manufacture them. This is a recording of the expressly reported Action 1
capability PASS, not a replacement receipt or a complete native qualification claim.

- RESULT=PASS_READ_ONLY_CAPABILITY_INVENTORY; PE73_ACTION1_EXIT_STATUS=0; issues=[].
- production_authorization=false; native_qualification_complete=false.
- Host nutandpihole; UID/GID1000:1000; Linux6.12.47+rpt-rpi-v8; aarch64;
  CPython3.11.2. Reported symbols, dir_fd support, flock and renameat2 symbol present.
- Package directory owner/group1000:1000, mode0755, ACLs absent.
- Known cron entry counts=[1,1,1]. Scheduler SHA256
  3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
- Process entries202:38 readable executable links,163 unresolved,1 vanished.
  The counts reconcile:38+163+1=202. complete_caller_coverage=false;
  cached_modules/open_readers_excluded=false. Unresolved does not mean163 known
  HIOC callers or163 unsafe processes; it is a discovery/attribution limitation.
- Operator reports no production changes. Codex performed no PI3/PI5 access.

Disposition: reported read-only capability check PASS with its source limitations.
Q01 environment floor is supported by the summary; Q02/Q04 symbol exposure and Q07
package ACL absence are reported capabilities/observations only, not behavioral tests.
Q08 known scheduler lines/hash are supported; implementation/editor exclusivity and
actual cron interpreter remain unresolved. Q09 visibility is partial. Q11-Q15 fence,
privilege, complete drain, persistence, actual native recovery/rollback/release are
not established. No new production permission, fresh operation authorization or
closure follows from Action 1 PASS. Do not request a repeat of established observations.

#### Exactly one proposed next action: isolated descriptor/create/no-follow fixture

This is only the smallest first part of the existing isolated experiment1 (Q02/Q03,
basic Q06/Q07). It is independent of the unresolved production privilege boundary.
No root helper, mode0000, production fence or Windows seam change is needed.
It does not qualify error-injected descriptor cleanup, atomic replacement, fsync,
flock, scheduler editing, process drain, cached modules or actual controller recovery.
Those remain separately gated; this command does not chain into them.

EXPLICIT SEPARATE AUTHORIZATION REQUIRED BEFORE RUNNING: approve this exact block on
PI3 NUT&PIHOLE as jazofv1, its runtime-generated single new private
/home/jazofv1/.hioc-pe73-native-<uuid> directory, one0600 constant-data probe, one
scratch symlink, descriptor-relative read/write/exclusive-create/no-follow checks,
and deletion of only its identity-bound created objects/directory. Review requires
no concurrent manipulation of that private fixture. No chmod/chown, cron, services,
locks, fsync, rename, subprocesses, signals, production writes, HIOC imports, network,
credentials or engine execution is permitted. Production target access is limited
to a no-follow metadata lookup for scratch device comparison. No sudo or root.
The current user instruction authorizes preparation, not execution of this block.

Location and cleanup follow the prepared qualification boundary. The command creates
nothing until target/identity/parent checks pass. A primary or cleanup failure cannot
produce PASS. Unexpected identities/content are retained privately, with exact
basename/device/inode in the receipt for separate inspection/disposition. No recursive
or prefix-based deletion, automatic retry or cleanup of a prior fixture occurs.
Descriptor close is attempted once per acquisition, never retried after close failure.
If killed externally, retain the scratch fixture and STOP; no cleanup-by-guessing.

Future operator: machine PI3 NUT&PIHOLE, user jazofv1, any working directory.
DO NOT RUN until the separate isolated-mutation authorization above is granted.

```sh
/usr/bin/python3 -I -S -B - <<'PY'
import datetime
import errno
import json
import os
import platform
import socket
import stat
import sys
import uuid

r = {"kind": "ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW", "production_modified": False,
     "native_qualification_complete": False, "STOP_REQUIRED": True,
     "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
owned = []
acquired = attempts = 0
close_errors = []
checks = []
primary = None
cleanup = "NOT_CREATED"
home = root = None
leaf = None
anchor = None
created = False
nodes = {}
def fail(code):
    raise ValueError(code)
def opened(path, flags, mode=0o777, parent=None):
    global acquired
    f = os.open(path, flags, mode, dir_fd=parent)
    owned.append(f)
    acquired += 1
    return f
def close_once(f):
    global attempts
    owned.remove(f)
    attempts += 1
    try:
        os.close(f)
    except OSError:
        close_errors.append("CLOSE_NOT_CONFIRMED")
        raise
def node(s):
    return (s.st_dev, s.st_ino, s.st_uid, s.st_gid, stat.S_IFMT(s.st_mode))
def secure_dir(f):
    s = os.fstat(f)
    if not stat.S_ISDIR(s.st_mode) or s.st_uid not in (0, 1000) or stat.S_IMODE(s.st_mode) & 0o7022:
        fail("UNSAFE_DIRECTORY")
    for name in ("system.posix_acl_access", "system.posix_acl_default"):
        try:
            os.getxattr(f, name)
        except OSError as e:
            if e.errno != errno.ENODATA:
                fail("ACL_NOT_ESTABLISHED")
        else:
            fail("ACL_PRESENT")
    return s
try:
    if socket.gethostname() != "nutandpihole" or platform.system() != "Linux" or sys.version_info < (3, 10):
        fail("TARGET_OR_PYTHON_MISMATCH")
    if (os.getuid(), os.geteuid(), os.getgid(), os.getegid()) != (1000, 1000, 1000, 1000):
        fail("IDENTITY_MISMATCH")
    r["environment"] = {"kernel": platform.release(), "architecture": platform.machine(),
        "python": platform.python_version(), "interpreter": sys.executable, "uid": 1000, "gid": 1000}
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    home = opened("/", flags)
    secure_dir(home)
    for part in ("home", "jazofv1"):
        child = opened(part, flags, parent=home)
        secure_dir(child)
        old = home
        home = child
        close_once(old)
    s = secure_dir(home)
    if (s.st_uid, s.st_gid) != (1000, 1000):
        fail("HOME_IDENTITY_MISMATCH")
    runtime = os.stat("hioc", dir_fd=home, follow_symlinks=False)
    if not stat.S_ISDIR(runtime.st_mode):
        fail("RUNTIME_DEVICE_NOT_ESTABLISHED")
    leaf = ".hioc-pe73-native-" + uuid.uuid4().hex
    os.mkdir(leaf, 0o700, dir_fd=home)
    created = True
    root = opened(leaf, flags, parent=home)
    anchor = secure_dir(root)
    r["fixture"] = {"basename": leaf, "device": anchor.st_dev, "inode": anchor.st_ino,
        "uid": anchor.st_uid, "gid": anchor.st_gid, "mode": format(stat.S_IMODE(anchor.st_mode), "04o")}
    if (anchor.st_uid, anchor.st_gid, stat.S_IMODE(anchor.st_mode)) != (1000, 1000, 0o700) or anchor.st_dev != runtime.st_dev:
        fail("FIXTURE_IDENTITY_OR_DEVICE_MISMATCH")
    f = opened("probe", os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, root)
    s = os.fstat(f)
    nodes["probe"] = node(s)
    if not stat.S_ISREG(s.st_mode) or (s.st_uid, s.st_gid, stat.S_IMODE(s.st_mode), s.st_nlink) != (1000, 1000, 0o600, 1):
        fail("PROBE_IDENTITY_MISMATCH")
    raw = b"PE73_ISOLATED_CONSTANT_PROBE\n"
    if os.write(f, raw) != len(raw):
        fail("SHORT_WRITE")
    os.lseek(f, 0, os.SEEK_SET)
    if os.read(f, len(raw) + 1) != raw:
        fail("PROBE_READ_MISMATCH")
    close_once(f)
    checks.append("ANCHORED_PRIVATE_CREATE_READ")
    try:
        f = opened("probe", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, root)
    except FileExistsError:
        checks.append("EXCLUSIVE_CREATE_COLLISION_REFUSED")
    else:
        close_once(f)
        fail("EXCLUSIVE_CREATE_COLLISION_ACCEPTED")
    os.symlink("probe", "probe-link", dir_fd=root)
    nodes["probe-link"] = node(os.stat("probe-link", dir_fd=root, follow_symlinks=False))
    try:
        f = opened("probe-link", os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, parent=root)
    except OSError as e:
        if e.errno != errno.ELOOP:
            fail("NOFOLLOW_RESULT_NOT_ESTABLISHED")
        checks.append("SYMLINK_NOFOLLOW_REFUSED")
    else:
        close_once(f)
        fail("NOFOLLOW_ACCEPTED_SYMLINK")
except Exception as e:
    primary = {"type": type(e).__name__, "code": str(e) if type(e) is ValueError else "ISOLATED_OPERATION_FAILED"}
finally:
    if created:
        cleanup = "INCOMPLETE_RETAIN_FIXTURE"
        r["fixture_basename"] = leaf
        try:
            if root is None or anchor is None:
                fail("CLEANUP_ANCHOR_UNAVAILABLE")
            if node(os.stat(leaf, dir_fd=home, follow_symlinks=False)) != node(anchor) or node(os.fstat(root)) != node(anchor):
                fail("CLEANUP_DIRECTORY_DRIFT")
            names = os.listdir(root)
            if set(names) != set(nodes) or not set(names) <= {"probe", "probe-link"}:
                fail("CLEANUP_CONTENT_DRIFT")
            for name in names:
                s = os.stat(name, dir_fd=root, follow_symlinks=False)
                if node(s) != nodes[name] or (s.st_uid, s.st_gid) != (1000, 1000):
                    fail("CLEANUP_NODE_DRIFT")
                if not (stat.S_ISREG(s.st_mode) or stat.S_ISLNK(s.st_mode)):
                    fail("CLEANUP_UNEXPECTED_TYPE")
            for name in names:
                os.unlink(name, dir_fd=root)
            os.rmdir(leaf, dir_fd=home)
            cleanup = "EXACT_FIXTURE_REMOVED"
        except Exception:
            cleanup = "INCOMPLETE_RETAIN_FIXTURE"
    for f in list(reversed(owned)):
        try:
            close_once(f)
        except OSError:
            pass
r["checks"] = checks
r["primary_failure"] = primary
r["cleanup"] = cleanup
r["descriptor_acquisitions"] = acquired
r["descriptor_close_attempts"] = attempts
r["descriptor_close_errors"] = close_errors
ok = primary is None and cleanup == "EXACT_FIXTURE_REMOVED" and acquired == attempts and not close_errors and len(checks) == 3
r["RESULT"] = "PASS_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW" if ok else "FAIL_STOP_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW"
r["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps(r, sort_keys=True, separators=(",", ":")))
raise SystemExit(0 if ok else 1)
PY
```

Immediately afterward, before another command, capture the exit status in the shell:

```sh
pe73_isolated_status=$?
printf 'PE73_ISOLATED_EXIT_STATUS=%s\n' "$pe73_isolated_status"
```

Expected format: one sanitized JSON receipt; RESULT=PASS_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW
and exit0 only if all three checks, exact cleanup and descriptor close accounting pass.
Otherwise FAIL_STOP_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW and exit1. Report primary
failure and cleanup independently. Receipt contains native environment and scratch
identity, no Asset/configuration/private scheduler contents. This is scratch-only
ISOLATED_NATIVE evidence, not proof of the production fence or caller exclusion.
Actual isolated result is NOT_EXECUTED; no authorization is inferred from this proposal.

The supplied Action 1 summary is retained exactly in meaning and no original receipt
is rewritten. Only existing PE-7 evidence/current Master Plan and their two necessary
successor documentation identity bindings change. Accepted controller/tests,13 artifact
identities,39 successor identities and449 protected identities remain preserved.
Exactly one next action: obtain separate authorization for the single isolated
fixture block above. Do not access PI3/PI5, execute it, stage, commit, push or start
another qualification action as part of this recording/preparation assignment.

Local preparation validation: operator Python AST/compile and restricted call-surface
checks PASS. Five fully mocked Windows cases PASS: success; operation failure; close
failure; unexpected symlink-follow success; unexpected scratch content. Expected
results were one successful receipt and four fail-closed receipts, all descriptors
receiving one close attempt; unknown fixture content was retained. No Linux command
or native filesystem test ran. Prepared isolated command SHA256:
2cca26c2efad5d9394dac8b82e98a17c207582434a8240d07f1abc8fd1686724.


### PE-7.3 isolated descriptor/create/no-follow result and fence-access qualification

Classification: CURRENT. PE73_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW=PASS_OPERATOR_SUPPLIED.
NATIVE_QUALIFICATION=INCOMPLETE; NATIVE_DEPLOYMENT=BLOCKED;
PRIVILEGED_MAINTENANCE=BLOCKED; NATIVE_ROLLBACK=BLOCKED.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. No native refusal gate changes.
This supersedes the prior proposal's NOT_EXECUTED/next-authorization statements
only for this completed isolated test; the original proposal and command are retained.

#### Operator-supplied actual result, 2026-10-23

Source: the operator's current supplied result summary, not Codex-observed PI3 data.
No complete original JSON receipt, receipt digest, precise observation interval or
scratch basename/device/inode was supplied in this message. Do not reconstruct them.
The prior prepared command identity is retained in its preparation evidence; this
summary does not independently establish the exact executed command bytes.
No repeat of the completed test is requested.

- RESULT=PASS_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW.
- PE73_ISOLATED_EXIT_STATUS=0; date2026-10-23; host nutandpihole; UID/GID1000:1000.
- Checks passed: ANCHORED_PRIVATE_CREATE_READ;
  EXCLUSIVE_CREATE_COLLISION_REFUSED; SYMLINK_NOFOLLOW_REFUSED.
- Descriptor acquisitions=5; descriptor close attempts=5; descriptor close errors=[].
- Primary failure=null; cleanup=EXACT_FIXTURE_REMOVED.
- production_modified=false; native_qualification_complete=false.

Disposition: PASS for the reported isolated descriptor/create/no-follow operations.
The summary supports successful scratch behavior and close-attempt accounting for
that execution; it does not establish all descriptor failure paths, native atomic
replacement/fsync, production permission enforcement, drain or actual recovery.
It supplies partial native Q02/Q03/Q06 evidence, not complete qualification of those
rows. Prior Action 1 PASS remains OPERATOR_SUPPLIED with its recorded limitations.
The163 unresolved process observations remain unresolved; no owner/privileged/cached
module/open-reader exclusion follows from either PASS. No power-loss, universal
absence-of-transient-effects or complete production audit claim is made.

#### Exactly one remaining next action: isolated UID1000 mode0000 access feasibility

This is a bounded part of the existing isolated permission experiment3, directly
addressing Q06/Q11/Q12; it is not a new phase or a repetition of the completed test.
Separately authorize one operator-executed scratch DAC/access characterization as
jazofv1 on PI3 NUT&PIHOLE. It must test this exact conflict rather than unrelated
atomicity/cron/process-discovery questions:

1. In one new private /home/jazofv1/.hioc-pe73-native-<random> fixture (root0700,
   UID/GID1000:1000, secure no-follow ancestors), create a child package directory
   matching the reported original0755 and a constant private regular probe. Bind
   root/child device, inode, owner/group/mode/ACL absence; verify filesystem identity.
2. Before restriction, retain an ordinary read-only file descriptor to that probe
   and an open directory descriptor to the child; no production descriptors/imports.
3. Apply mode0000 ONLY to that created child via its pinned descriptor. Observe,
   without changing effective identity, whether a new pathname open, a new child open
   relative to the retained directory descriptor and a new exclusive child create
   are denied. A directory fd must not be assumed to confer traversal permission.
4. Observe whether the already-open file descriptor can still read the constant
   fixture bytes. This tests a known exclusion limitation, not a safe delivery bypass.
5. As the same owner, restore ONLY that child's recorded original0755 via its pinned
   descriptor, then verify original identity/mode and new ordinary access. Owner
   restoration demonstrates why the fence also requires permission-editor exclusion.
6. Record expected versus actual errno/results, kernel/interpreter/UID/GID, effective
   capability disposition if needed to explain unexpected access, and exact fixture
   identities, primary outcome, restoration, descriptor accounting and cleanup.
   Missing/ambiguous observations are INSUFFICIENT_EVIDENCE, not invented denial.

Expected characterization (NOT an observed result yet): mode0000 denies new lookup/
creation to the ordinary UID1000 process, even with the retained directory fd, while
an already-open file can remain readable and the owner can restore permissions.
Successful characterization documents BOTH the controller-write conflict and the
insufficiency of this fence alone against retained access/owner edits. Unexpected
access or failure to verify restoration stops; it never authorizes installation.
No new privilege or file-descriptor workaround is selected by this experiment.

SEPARATE EXPLICIT AUTHORIZATION REQUIRED before any scratch mutation: one exact
bounded operator procedure permitting only creation of that unpredictable private
fixture/probe, pinned child-only0755->0000->0755, the stated access attempts and
identity-bound cleanup. Allow no root/sudo, new privileged mechanism, permissions on
production paths, production open/write attempts, controller execution, HIOC imports,
cron, services, locks, network, credentials, signals or other native tests.
This recording assignment does not authorize or execute that action.

The procedure must use independent primary/restoration/cleanup outcomes. Restore the
created child through its retained descriptor in finally, including a failed access
assertion; preserve the primary failure if restoration or cleanup also fails. Delete
only explicitly created identity-bound fixture objects, then empty created dirs;
no recursive or prefix deletion. On unexpected identity/content or incomplete
restoration/cleanup, retain the exact private fixture and receipt and STOP for
separate disposition. Do not retry or change production to make the test pass.

Why this is next: it verifies the actual native permission assumptions that determine
whether an unprivileged writer can operate behind the proposed closed-directory fence.
The accepted controller requires UID/GID1000 and NativeFS.directory needs traversal.
Root-running it violates TARGET_IDENTITY; preopening a directory fd is not established
as sufficient access. Even the expected test outcome does not resolve privilege/
caller coordination: it bounds the missing capability for a later separately authorized
solution. No design change or production enablement is inferred. Native deployment,
privileged maintenance, rollback and release remain blocked; PE-7.4 NOT_AUTHORIZED.

Only existing implementation evidence/current Master Plan and their two necessary
successor document identities change. Accepted controller/tests and all13 delivery,
39 successor and449 protected identities are preserved. No completed native tests or
historical suite rerun; no PI3/PI5 access, production change, stage, commit or push.
Exactly one next action: separate authorization for the isolated UID1000 mode0000
access-feasibility experiment specified above. Stop after recording this result.


### PE-7.3 mode0000 native result and bounded deployment-access decision

Classification: CURRENT. PE73_MODE0000_ACCESS=PASS_OPERATOR_SUPPLIED.
NATIVE_QUALIFICATION=INCOMPLETE; DEPLOYMENT_ACCESS_RESOLVED=FALSE.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. Native deployment, privileged maintenance,
rollback and consumer release remain blocked. Earlier proposals/receipts are preserved;
this result supersedes only the preceding planned mode0000 experiment's pending status.

#### Actual operator-supplied mode0000 result, 2026-10-23

Source: the user's supplied PI3 summary; not Codex-observed production evidence.
No original complete JSON, execution digest, exact interval or scratch device/inode
values were supplied here. Do not reconstruct or invent them. No completed test rerun.
The exact supplied facts are retained below; expected results are not substituted.

```ini
EVIDENCE_SOURCE=OPERATOR_SUPPLIED
DATE=2026-10-23
RESULT=PASS_ISOLATED_UID1000_MODE0000_ACCESS_CHARACTERIZATION
PE73_MODE0000_EXIT_STATUS=0
HOST=nutandpihole
UID=1000
GID=1000
PYTHON=3.11.2
KERNEL=6.12.47+rpt-rpi-v8
pathname_directory_open=DENIED
pathname_directory_open.errno=13
pathname_file_read=DENIED
pathname_file_read.errno=13
pathname_file_create=DENIED
pathname_file_create.errno=13
retained_dirfd_file_read=DENIED
retained_dirfd_file_read.errno=13
retained_dirfd_file_create=DENIED
retained_dirfd_file_create.errno=13
retained_file_descriptor_read=true
owner_restoration.fd_mode_restored=true
owner_restoration.named_identity_verified=true
fresh_path_read_after_restoration=true
cleanup.status=EXACT_FIXTURE_REMOVED
cleanup.error=null
descriptor_acquisitions=8
descriptor_close_attempts=8
descriptor_close_errors=[]
primary_failure=null
production_modified=false
complete_consumer_exclusion_established=false
native_qualification_complete=false
production_deployment_ready=false
```

Disposition: reported isolated access characterization PASS. It demonstrates the
UID1000 fresh-access conflict for the tested environment and that a retained directory
fd is not a bypass; retained file access survives and the owner can restore permissions.
Owner restoration and cleanup are reported verified for this fixture. It is not a
native-controller run, a complete drain certificate, a production security audit,
power-loss evidence or proof that a privileged publisher/broker works. Prior163
unresolved process observations remain unresolved; do not infer which are HIOC callers.

#### Bounded design assessment: compatibility evidence and alternatives

Assessment scope: existing Controller, NativeFS, NativeConsumers and maintenance seam,
not a redesign of PE-7.1 or a production implementation. Repository facts:

- tools/hioc-pe73-pi3-delivery.py Controller.__init__(fs, source, consumers) already
  injects filesystem/consumer objects; the tests exercise this seam with fixtures.
  This establishes an extension seam, not a qualified privileged backend.
- NativeFS.directory reopens secure no-follow ancestors; snapshot/read traverse the
  package. Controller.commit performs preflight and post-publication observations,
  then verify snapshots the entire installed set. Recovery and rollback also read
  and compare exact current snapshots. A publisher-only exception cannot satisfy
  these reads. Journal, backup/staging and full parent identities must still agree.
- main fixes real/effective UID/GID1000 and instantiates NativeFS/NativeConsumers
  directly. No accepted CLI switch selects a broker or bypasses native refusal.
  NativeFS rejects ACLs and requires exact1000:1000 regular-file ownership/modes.
- NativeConsumers cannot establish complete independent-caller exclusion. A new
  access backend would not itself qualify or authorize consumer maintenance.

The Linux manuals corroborate platform semantics only, not PI3 capability observations:
[capabilities(7)](https://www.man7.org/linux/man-pages/man7/capabilities.7.html)
describes DAC-bypass capabilities, which are not a13-path application allowlist;
[mount_namespaces(7)](https://www.man7.org/linux/man-pages/man7/mount_namespaces.7.html)
describes distinct process mount views, not automatic confinement of all callers.
The actual denials/restoration/retained-file behavior above remains OPERATOR_SUPPLIED.

Each option is assessed on all requested boundaries. Conditional possibilities below
are design inferences, not selected/installed mechanisms or proven native viability.

| Option / existing-controller compatibility | Existing consumers and independent callers / retained fds | Privilege and identity | Crash persistence | Partial publication / rollback | Existing services | Complexity / disposition |
| --- | --- | --- | --- | --- | --- | --- |
| Temporary publisher restricted to final replace only | Cannot itself drain cached readers, independent callers or retained descriptors; mode0000 still needs owner/editor/privileged exclusion. | Privileged replace may cross DAC, but UID1000 controller cannot perform required pre/post reads and snapshots. Root-created artifacts would violate ownership unless securely prepared as1000:1000. | Helper death must not restore access; retained fence/intent still require qualified recovery. | Existing journal requires observed installed identities, stage/backup validation and rollback reads/removal; publisher alone leaves these blocked. No external publication behind journal's back. | Shared consumers still require explicit bounded maintenance; Pi-hole/Unbound/NUT must remain unaffected. | Small apparent helper, incomplete solution. Not viable as a drop-in. |
| Temporary fixed-scope filesystem broker at the existing fs seam (expanded publisher candidate) | Separates authorized package access from ordinary new access, but does not exclude retained fds/modules, manual launchers or owner/privileged edits; complete maintenance proof remains mandatory. | Keep Controller/journal orchestration unprivileged UID1000; a distinct narrowly bounded authority would serve only necessary reads/snapshots and publication/restoration operations for pinned artifacts/ancestors. Exact1000:1000 results required. No privileged controller, arbitrary paths, shell or generic filesystem service. | Fence/journal must outlive either process. Lost/uncertain responses must stop, never retry/adopt/release; fresh attachment and authenticated recovery needed. None is implemented. | Must preserve the same intent->effect->observed fingerprint sequence,13 targets, five backups/eight absences, order, parent identities and explicit rollback. Both writes and observations need coverage; no second journal. | Only explicitly approved affected HIOC consumers paused; no unrelated service changes. Backend cannot imply pause or release permission. | Moderate, finite access boundary exploiting an existing seam. Smallest candidate worth a bounded prototype; not yet proven viable. CLI/native integration and contract delta need separate authorization. |
| Give the whole controller root or transient DAC-bypass capabilities | Still does not drain old readers or constrain other owner/privileged actors. A matching UID or cron hash is not caller exclusion. | Root violates TARGET_IDENTITY. A UID1000 capability-bearing interpreter could retain UID checks but grants broader DAC authority; it is not13-path isolation, and code/requester integrity is unresolved. No capabilities applied here. | Privilege lifetime does not supply durable exclusion or recovery. Process death must leave exact uncertainty/fence evidence. | Full privileged Python/filesystem surface and ownership/rollback behavior need new proof; existing refusal gates still block. | Does not remove need for approved pauses; capability scope could affect unrelated files/services. | Few visible code changes but materially broader authority/security burden. Not recommended as the minimal safe change. |
| Substitute ACL/group/mode or per-process mount/LSM isolation | Same UID1000 owner rule cannot distinguish ordinary controller from other same-UID callers. Per-process views/policy might separate launches, but existing processes/fds and all entrypoints still require drain/coverage. | ACLs conflict with NativeFS ACL rejection. Changed ownership/modes/views can conflict with exact observed metadata. Namespace/LSM policy is unqualified and not supplied by current controller. | Persistent enforcement, supervisor/namespace lifetime, editor/bypass coverage and restart behavior require a new native enforcement design. | All accesses must refer to the same real targets and retain expected ancestry/identities; view mismatch or global read-only state cannot silently substitute for the journal contract. | Wider launcher/mount/security-policy changes risk more consumers; no assumption that Pi-hole/Unbound/NUT can be stopped. | More surrounding infrastructure than a finite backend. No evidence supports drop-in compatibility; not selected. |
| Complete enforced HIOC-consumer quiescence while leaving package accessible to UID1000 | Could avoid the DAC writer conflict only if every affected process/launcher/editor is genuinely excluded and cached/open readers drained. Three cron locks/manual assurances do not establish that;163 unresolved observations remain. | Leaves controller/ownership contract intact, but enforcement of same-UID manual/privileged launchers is not implemented. A cooperative lock is not a replacement for accepted external exclusion. | Requires a crash-persistent launch boundary independent of controller/SSH and explicit release; merely stopping jobs is insufficient. | Existing Controller transaction could be reused only under a separately accepted real boundary; no automatic rollback or mixed-version restart. | Requires approved pauses of all affected HIOC consumers; preserve unrelated services and accepted missed-cycle/no-catch-up rules. | Conceptually simple but unbounded until complete enforced coverage is evidenced. Not a currently supported alternative to the persistent fence. |

Decision: none of the options is currently qualified for production, and no mechanism
in the unchanged accepted CLI resolves this conflict. Merely reopening the package
between operations, keeping a directory fd, restoring its mode early, using flock,
or calling chmod under a new label is not an accepted solution. A broker is an access
solution candidate, not proof that the fence constitutes complete consumer exclusion.

#### Exactly one next bounded action and required separate authorization

Recommend one PE-7.3 repository-only action: prepare an explicit access-contract delta
and a NONPRIVILEGED, fixture-only prototype of a transaction-bound filesystem broker
adapter at the existing Controller.fs seam, then validate it with focused synthetic
fault/negative tests. This is one bounded engineering action inside PE-7.3, not an
additional review phase, native deployment or implementation of a privileged helper.
It requires separate authorization for new repository prototype/test/document bytes
and any proposed accepted-contract change. No authorization is inferred here.

The finite prototype must establish a go/no-go result for precisely:

- Complete required call coverage: ancestor/security observations, bounded read/
  snapshot, approved staged/temp creation, publication, verification, removal and
  rollback under held maintenance. Keep ordinary accessible journal/backup operations
  under existing UID1000 authority where possible. Do not assume replace alone is enough.
- Fixed manifest paths/identities and canonical bounded data, never arbitrary caller
  paths, descriptors, commands, credentials/config/state reads or global filesystem APIs.
  Exact allowed ancestor/temp paths and operation ordering must be enumerated explicitly.
- Preserve13 artifact pins, UID/GID1000 final ownership, five backups/eight absences,
  dependency/incident-last ordering, descriptor/no-follow guards, exact fingerprints,
  fsync/uncertainty semantics and the existing single journal as transaction authority.
- Authentication/authorization design must not treat UID1000, PID alone, matching
  JSON/reference or a successful receipt as trusted permission. Actual transport,
  requester/code integrity and future least-privilege enforcement are unresolved
  contract requirements, not invented mechanisms. No secret or credential is created.
- Duplicate/stale/forged/out-of-order/out-of-scope requests, drift and dropped replies
  must fail closed. Kill/lost-result ambiguity must remain pending rather than being
  adopted or replayed. Explicit fresh recovery/rollback/release authorization is retained.
- Do not modify accepted controller/tests or contract in place, enable the real CLI,
  introduce root/sudo/capabilities, install a helper/service, contact PI3/PI5, change
  production or turn off existing native refusal. Prototype success proves interface/
  transaction behavior only; later actual privilege qualification remains separate.

If the prototype cannot preserve unchanged Controller behavior/identities, or needs
broader authority than this finite scope, STOP with the exact incompatibility instead
of quietly expanding the helper, changing historical authority or relaxing consumer
exclusion. This recommendation has not implemented a broker or authorized production.

Only existing PE-7 evidence/current Master Plan and directly necessary two-document
successor identities are updated by THIS action. No tests rerun; no controller/test
changes, PI3/PI5 access, production mutation, stage, commit or push. All13 artifact,
39 successor and449 protected identities remain valid. PE-7.3 remains IN_PROGRESS;
PE-7.4 NOT_AUTHORIZED. Next action is only the separately authorized fixture prototype
and explicit access-contract delta described above.


### PE-7.3 experimental filesystem-broker feasibility candidate

Classification: CURRENT EXPERIMENTAL, repository-only and nonproduction.
The accepted controller0589cf6363626d14ab9abe08c001ddef634b243326513b27de43a7b93aa4f95f
and accepted tests4fef3799a3bae5733056fa30b3423bca656026103a6ce02e443e14ac639ce281
remain byte-identical. The accepted PE-7 contract is unchanged; the proposed delta
below is not adopted. Native deployment, maintenance, rollback and release stay blocked.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. No production architecture is approved.

New standalone files (only two): tools/pe73_filesystem_broker_prototype.py and
 tests/test_pe73_filesystem_broker_prototype.py. The entry is a Windows fixture factory,
not a command-line utility, service, socket, helper, production root override or installer.
It creates its own unique Windows temporary root, with real temporary file bytes and
explicit synthetic POSIX owner/mode metadata. Such metadata is a fixture observation,
not native Linux permissions. No operational credentials or private production data.

#### Architecture, exact seam and operation coverage

The accepted controller file is locally hash-verified and loaded unchanged into one
private module instance. Only that instance's identity constants become synthetic:
identical13 artifact names/order/modes and five replacement roles/eight absence roles,
synthetic source/baseline bytes, synthetic source SHA/Git blobs/release and fixture cron
labels. No real release/historical runtime bytes are used as fixture payloads. Accepted
controller methods themselves are not copied or rewritten; Controller(fs,source,consumers)
executes preflight, prepare, publication, verification, rollback and inspection.
This is a feasibility exercise with synthetic constants, not production integration.

Components: Fixture owns the temporary disk; FixtureDisk implements its finite local
resources; BrokerFS adapts the actual accepted filesystem seam; Broker exposes seven
artifact operations; FixtureAuthority validates controller-owned journal context and
issues single-use in-process object grants/replies; FixtureConsumers is a distinct
externally held SYNTHETIC_ONLY boundary. Broker cannot establish or release that boundary.
All operations are scoped to exact13 artifact identifiers, their computed stage/backup
slots and fixed temporary names/ancestors; no user-supplied root, arbitrary path or shell.

| Required operation | Representation / authority |
| --- | --- |
| Anchored traversal | No-follow/reparse/regular-single-link checks of real temporary paths and captured parent device/inode; explicit synthetic UID/GID/mode policy. No claim of native POSIX dir_fd enforcement on Windows. |
| Source identity | Exact synthetic manifest SHA256/Git blob verification through accepted check_sources; no real production payload read. |
| Five existing/eight absent targets | Broker snapshots expose full current identities or absence; accepted preflight verifies synthetic baselines. |
| Existing target reads | READ returns only bounded known synthetic baseline/candidate contents, hash-bound to the observed source/target context. |
| Backup and staging | BACKUP/STAGE map to one computed slot per artifact; original baseline and previous-stage/backup preconditions enforced. No generic write operation. |
| Publication/verification | PUBLISH follows the accepted pending path/installed prefix, uses verified source/stages/backups and returns the actual installed snapshot. Controller alone records progress; all13 paths verified. |
| Recovery inspection | Fresh broker/authority/adapter/controller reopen actual retained temporary bytes and synthetic metadata; current snapshots are compared with the original controller journal. No prior reply or grant is trusted. |
| Rollback | RESTORE uses verified five original backups; REMOVE only applies to authorized newly installed artifacts, in controller-defined reverse order. Controller records restored provenance. |
| Drift/uncertainty | Exact expected snapshots and current journal context gate mutations; no automatic retry/adoption. Read-only inspection may report drift without authorizing any mutation. |

The adapter must not read protected target metadata locally to construct a broker
request: that would assume the DAC bypass being investigated. Observation requests
bind controller-recorded evidence (or explicitly unknown preflight observations),
then the broker performs protected inspection. Mutation requests bind exact recorded
preconditions/absence. The prototype tests this access separation explicitly.

The journal and original backups are outside the proposed package fence. To avoid
recursive broker authorization while the accepted _journal validator reads rollback
backups, a stateless read-only invocation of that SAME accepted validator uses the
local evidence view. It never writes phase/progress. A derived validation cache is
keyed by freshly secured journal bytes AND identity on every use; a changed key is
revalidated, and a fresh broker starts with no cache. This is not a second authority.

#### Closed interface, authorization and request/reply evidence

Closed request fields: version, operation, artifact, area, transaction, operation_id,
source_sha256, expected, context, payload_hex. version is exact integer1; transaction
is the single SYNTHETIC_PE73_BROKER_V1; operation_id is a unique32 lowercase-hex value.
operation is SNAPSHOT, READ, BACKUP, STAGE, PUBLISH, RESTORE or REMOVE. area is TARGET,
STAGE or BACKUP with operation-specific restrictions. Artifact is an exact allowlisted
name, never an absolute/substituted/traversal/backslash path. Payload is bounded and
allowed only for verified backup/staging bytes. Source identities and expected state
are bound; context contains current controller journal digest, relevant controller
prepare/commit/rollback authorization reference and external fixture session.
Duplicate JSON keys, unknown fields/operations/types and nonfinite/noncanonical input
are rejected. A transaction string, UID, phase label or receipt alone is not permission.

Closed reply envelope: version, transaction, operation_id, request_sha256, result,
synthetic_only=true. Results are bounded synthetic read content/hash or snapshots.
An independently issued in-process object grant binds the exact request digest and
is consumed once; replies are checked against the actual sealed reply object/digest
and request identity. Copied/modified/forged replies are not accepted. These object
identities are fixture capabilities ONLY, not production IPC authentication, credential
issuance, same-UID isolation, code integrity or cryptographic Linux peer authentication.

The original controller journal remains sole phase/order/provenance/recovery authority.
The broker never writes it, authorizes rollback/release, changes permissions, activates
cron, starts processes or executes engines. Its narrowly bounded attempt records are
NONAUTHORITATIVE_ATTEMPT_ONLY: negative replay evidence binding request/intent IDs.
They can refuse repeated uncertain mutations, including across a fresh broker, but
cannot establish installation, completion, recovery authorization or consumer release.
They carry no competing transaction phases. Fresh read-only inspection does not rely
on these records as positive evidence. Unknown/corrupt record state cannot grant access.

#### Proposed access-contract delta — NOT APPLIED OR ACCEPTED

This is an explicit experimental proposal, separate from the authoritative contract.
The actual accepted controller/test/contract files and native refusal gates are unchanged.

1. Replace only the assumption that UID1000 can locally traverse every package target
   while fenced. A future explicitly selected filesystem adapter would request narrowly
   bounded observations/effects; unprivileged Controller remains the journal orchestrator.
   The current CLI hardcodes NativeFS/NativeConsumers and offers no broker entry point.
   Any new native wrapper/selection/provider is an explicit future contract/authorization
   change; prototype success cannot enable it.
2. Enumerate exactly which target/ancestor reads, snapshots, staging/publication and
   restoration/removal operations cross a future privilege boundary. Ordinary accessible
   journal/backups remain UID1000 where possible; source pins, modes and final file
   ownership1000:1000 remain exact. A replace-only helper is insufficient.
3. Future authority would need actual search/read/write access through mode0000 plus
   tightly bounded creation/publication/removal and enforcement of1000:1000 final
   ownership. This does not select root, capabilities, arbitrary chown, ACL exceptions
   or any implementation. No such privilege is implemented or requested here.
4. Native requester/code integrity, authenticated request/result transport, replay/crash
   persistence, least-privilege restrictions and exact snapshot equivalence remain
   unimplemented. In-process object grants cannot be reinterpreted as native security.
   No secret, credential, sudoers rule, privileged daemon or permanent service is added.
5. Preserve a single controller-owned journal, current source/target/parent identities,
   all13 pins and ordering, five backups/eight absent targets, strict validation and
   explicit authorization. No broker-record-as-authority, implicit adoption or separate
   installation history. Lost replies remain unconfirmed effects until independently
   inspected; inspection is not permission to resume uncertain mutations.
6. Preserve all consumer-exclusion requirements. Mode0000 does not exclude owner edits,
   privileged callers, cached modules or retained file descriptors. External qualified
   drain, editor/launcher coverage and crash-persistent exclusion remain mandatory.
   Broker success must not reopen that boundary or authorize cron/release/evaluation.
7. Mandatory future native evidence: bounded real authority/transport and permitted
   operation proof under the actual fence; actual1000:1000 modes/ownership; secure
   descriptor/ACL/no-follow behavior; atomic replace/no-replace and file/directory fsync;
   process-loss/lost-reply and replay durability; independent journal-bound inspection;
   qualified fresh consumer exclusion and distinct rollback/recovery/release authority.
   Windows fixture PASS proves none of those native properties.

No irreconcilable controller-seam conflict has been waived. The finite adapter proposal
must stop if native result authentication, exact metadata semantics or scoped access
cannot preserve existing invariants. It must not quietly run the controller as root,
expand arbitrary filesystem authority or weaken maintenance requirements. Native
feasibility and the demonstrated production access conflict remain unresolved.


The proposed change explicitly delegates protected kernel-object observations from
local NativeFS to a separately trusted peer. Matching JSON fields/digests alone do
not authenticate that peer or prove its filesystem observations. A future authenticated
reply must bind the exact request/nonce/operation, transaction/authorization context,
source identity and observed target/ancestor identity; stale and cross-request replies
must be rejected. The concrete IPC, code/peer trust anchor and enforcement mechanism
are unresolved, not selected or claimed secure by this fixture experiment.

Future privilege budget (requirements, NOT granted privileges):

| Resource/operation | Rights that would need controlled provision |
| --- | --- |
| Fixed fenced ancestors and existing module files | Search/read access despite mode0000, no-follow anchored open and exact metadata/ACL inspection. No arbitrary directory or config/state/credential reads. |
| Fixed target-parent temporary creation and publication | Parent search/write despite mode0000; fixed exclusive temporary name; verified bytes, permitted mode and final1000:1000 ownership before acceptance; replace versus no-replace semantics. No generic rename/write API. |
| Exact installed new-file removal / replacement restoration | Same bounded parent search/write, exact installed identity, verified backup and controller rollback context. No arbitrary deletion or historical-journal cleanup. |
| Existing accessible journal/backup/source evidence | Ordinary UID1000 access retained where possible; no new privilege merely to control phase. Source/backup hashes and the same single journal remain mandatory. |
| Consumer fence, editors and privilege inheritance | Not broker authority. No chmod/restore/release, root-running controller or inherited broad capability; those independent gates remain blocked. |

A helper's actual execution identity and any ownership-setting privilege must be
separately justified; the prototype does not assume root-created files automatically
meet1000:1000. Broad DAC capabilities are not path restrictions. No root/capability/
chown grant is requested by this document. Linux directory fsync and no-replace,
post-crash trace durability and genuine native authority are not established here.
The accepted controller also refuses continuation of pending or already-restored
rollback states; this prototype provides inspection, not a new resume/repair API.
Unknown effects remain blocked for explicit disposition under existing authority.


#### Final focused validation, preservation and disposition

PE73_FILESYSTEM_BROKER_PROTOTYPE=PASS within the authorized experimental Windows
fixture scope. BROKER_ACCESS_CONTRACT_DELTA=PROPOSED_NOT_ADOPTED;
BROKER_NATIVE_INTEGRATION=NOT_AUTHORIZED. No production architecture/privilege approval.

Selection: unittest.defaultTestLoader.loadTestsFromName('test_pe73_filesystem_broker_prototype').
Established bundled Windows Python stdin harness, repository root, -B and UTF-8,
HIOC_TEST_SHELL cleared, shell-free PATH and sys.path[:0]=['tests','pi4/lib'].
Final result:54 run,54 passed,0 failures,0 errors,0 individual skips,0 class-level skips.
Unittest elapsed584.825 seconds; harness elapsed585.000 seconds. Direct result counts,
full failure detail list (empty) and pre/post source hashes are retained in temporary
hioc-pe73-broker-feasibility/prototype-result.json, independent of console truncation.

Final source identities, unchanged throughout this complete final run:

- tools/pe73_filesystem_broker_prototype.py SHA256 b7db2f55dd99fb1e7161a3afc054695bb5151b3866618dc8e2267afc0da47469.
- tests/test_pe73_filesystem_broker_prototype.py SHA256 3ee70a530e8b4b9e87ffed1fff4f56948b33e0abdccb22812ba2135b279bc791.

The14 observation tests assert a single actual accepted-controller synthetic full
prepare/commit/rollback workflow and each of its13 captured artifact outcomes (five
replacements/eight new). Additional focused cases cover every required mutation fault
boundary, independent fresh broker/authority/adapter/controller reconstruction, replay
across reconstruction, protected-access separation, identity/backup corruption, path/
symlink/reparse/type/hardlink substitution, source/mode/owner drift, closed schemas,
forged grants/replies, no-replace collision, explicit uncertainty and no consumer release.
Mocked symlink/reparse identification and synthetic owner/mode metadata are not claimed
as native Linux enforcement. No root, capabilities, network, engine or privileged backend.

Development-only checks are not final acceptance evidence: initial new smoke tests
found fixture canonical-framing and recursive journal/backup-validation issues, and a
new test's assumed rollback-report field was corrected. The final design uses the
accepted public canonical hashes and a stateless local evidence-validation view.
The separate broker-message canonicalization is sorted compact ASCII JSON without a
trailing newline; its context digest binds that canonical validated journal object,
not a replacement for the controller's public newline-terminated preflight/journal
hash. A development run was stopped to consolidate redundant full-path transactions
and add no-replace/result-schema checks; no partial run is reported as a final PASS.
Five narrow new guard tests passed before the complete54-test run. None of the
accepted104-test suite or full historical HIOC suite was rerun: their dependencies
and accepted controller/test bytes were not changed by this standalone prototype.

Only five paths change by this action: the two new prototype/test files above,
docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md, current docs/HIOC_MASTER_PLAN.md
and the directly necessary two documentation identities in the existing successor
record. No new governance record/schema, production contract change or extra framework.
The accepted controller/test/contract and historical evidence remain unchanged;
all13 actual delivery identities,39 successor identities and449 protected identities
are verified. Native refusal, runtime source/modes, five/eight roles and order remain
unchanged. git diff --check passes; zero staged and unexpected paths; stash unchanged.
Existing candidate now has three modified tracked files and four authorized untracked
files, including the two preexisting accepted controller/test files. No stage/commit/push.

Remaining requirements are explicit: native peer/code integrity, authenticated bounded
transport/results, scoped privilege and exact ownership/descriptor semantics, Linux
atomicity/durability, crash-persistent exclusion/anti-replay, complete caller/editor/
retained-reader coverage, fresh recovery/rollback/release authority and approved
native integration. Prototype PASS does not resolve those requirements or the
production mode0000 access conflict. No PI3/PI5 access, production files/permissions/
cron/services change, credentials, monitoring, migration, notifications or deployment.
PE-7.3 remains IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
Exactly one next bounded action: separately authorized focused independent acceptance
of this experimental feasibility prototype and its explicit unapplied contract delta,
inside the existing PE-7.3 checkpoint. No native helper implementation or production
operation is authorized by that recommendation. STOP_REQUIRED=TRUE.


### PE-7.3 guarded maintenance-window amendment proposal — NOT ADOPTED

Classification: PROPOSAL ONLY. PE73_MAINTENANCE_WINDOW_AMENDMENT=PROPOSED_NOT_ADOPTED.
This is a decision-ready implementation-level amendment, not deployment authority.
The authoritative PE-7 contract and accepted source files remain unchanged.
PE-7.1/7.2 COMPLETE/PASS; PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
Native commit, maintenance, privilege and rollback refusal gates remain in force.
No operator risk acceptance, production installation or consumer release is claimed.

#### 1. Original authority and exact existing implementation requirement

Original contract: [PE-7 consolidated contract](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md),
section 13 PE-7.3 row (line1016 in the unchanged accepted document), requires guarded
artifact/integration/UI/trust delivery with backups/rollback, exact paths/hashes/
modes/owners/ancestors and observed HA API/resource capability. Adapter/editing/
evaluator remain disabled except separately specified preflight; no recurring job
or automatic migration. Section12 C21/C23/C24 retains protected evidence, immutable
history, no unauthorized changes and independent acceptance. Section13 requires
separate checkpoint authorization. Sections12/14 retain truthful evidence and
missing-fact gates; these production validation requirements are not waived.

The original contract does not prescribe mode0000, a filesystem broker, quarantine
or universal kernel-enforced caller exclusion. Those are later implementation
mechanisms/assurances. Guarded installation and the original acceptance criteria
are preserved; no explicit original-contract conflict was identified in proposing
this limited assurance reduction. Any later discovered conflict stops adoption.
Explicitly approved maintenance pauses must not become a hidden PE-5 prerequisite
or an unauthorized producer/policy change (contract section12, lines992-995).

Exact existing wording, preserved above under "Consumer coordination: supplied
facts and deliberate native block", lines812-818 before this append:

~~~text
Synthetic success/failure/rollback uses an explicitly test-only, externally owned
consumer fence held independently of controller exceptions. This demonstrates
transaction behavior under that stated boundary; it does not supply a PI3 fencing
mechanism, universal caller exclusion or power-loss/process-crash safety evidence.
The independent partial-transaction exclusion prerequisite remains unresolved.
A future native coordinator must establish that boundary before publication can be
enabled; do not replace this gate with an operator boolean or inferred cron absence.
~~~

The matching later readiness requirement, lines838-841, and the current native
CONSUMER_COORDINATION_NOT_ESTABLISHED refusal express the same stronger assurance.
They remain historical/current implementation authority until explicit adoption;
this proposal does not silently rewrite them or make the old provider deployable.

#### 2. Complete proposed replacement wording

Proposed normative wording, to take effect ONLY after explicit operator adoption:

~~~text
During a separately authorized PE-7.3 maintenance window, publication and rollback
may use the existing UID-1000 controller only after exact approved scheduled
launches have been excluded and reobserved, known affected processes have been
identified and verifiably drained, and one named operator has accepted exclusive
maintenance responsibility and prohibited independent/manual affected commands.
Scheduled-launch exclusion is a verified technical control over the identified
scheduler entries. Manual-command restrictions are procedural controls, not
technically enforced exclusion. Draining covers the identified processes and
observed evidence only; it does not prove universal absence of cached modules,
retained descriptors, undiscovered processes or alternate launchers.

The authorization must explicitly acknowledge the residual risk of a
noncooperating independent caller or an affected process missed during drain.
This amendment does not claim complete consumer exclusion. It does not authorize
unexpected writes, mixed-version execution, service impact or acceptance without
the original mandatory evidence. Unresolved visibility limits and residual risks
must be stated; documentation alone does not accept them.

Exact scheduler preservation, source/target/security checks, all 13 artifact pins,
backups, dependency order, durable controller intent and verified progress,
independent filesystem inspection, and separately authorized rollback remain
mandatory. Controller failure, SSH loss, window expiry, pending publication or
interrupted rollback must never trigger automatic retry, adoption, rollback,
scheduler restoration or consumer release. The operator's no-launch restriction
continues until explicitly released. Reboot invalidates the maintenance readiness
assessment and requires fresh scheduler/process/runtime inspection before any
further mutation; no crash-persistent universal execution boundary is claimed.

Scheduler restoration and procedural consumer release require fully verified
installation or fully verified authorized rollback, exact current-state checks
and a fresh explicit release authorization. Unexpected scheduler modification,
known consumer activity, identity drift or insufficient mandatory evidence stops
dependent work without overwriting unreviewed state. The controller journal alone
never proves filesystem success, scheduler enforcement, process drain or safe
release. All other accepted PE-7 requirements remain unchanged.
~~~

#### 3. Reason, unchanged safeguards and reduced assurance

The existing-controls NO_GO establishes that cron/data locks do not prevent manual
imports and that native complete-drain/exclusion is unqualified. OPERATOR_SUPPLIED
mode0000 evidence establishes the UID1000 access conflict, not deployment readiness.
The proposed choice is practical maintenance with an explicitly lower assurance,
not a claim that technical universal exclusion has been solved.

Unchanged: exact accepted release51398bab4e2293b578b2cdac2d0740c3738cab2f, 13 paths,
five replacements/eight new targets, file ownership/modes/ancestor checks, verified
private backups/staging, dependency-first/incident-engine-last publication, atomic
individual operations, descriptor cleanup, source pins, strict journal/provenance,
fresh-process inspection and separate rollback authority. Preserve original
functional/protected evidence, no unexpected writes, no activation or migration,
no automatic recovery/release and all original production acceptance obligations.

Reduced: complete technically enforced independent-caller exclusion across partial
publication/controller failure becomes exact scheduled-launch exclusion plus
observed known-process drain and exclusive operator procedure. Cached/retained or
unidentified consumers and noncooperation remain residual risks. Risk acknowledgement
must name this reduction explicitly; a generic approval boolean is insufficient.
No currently unresolved risk is accepted by merely recording this proposal.

#### 4. Residual-risk classification and required response

| Event | Control and limitation | Required disposition |
| --- | --- | --- |
| Independent command during maintenance | PROCEDURAL prohibition; no technical manual-launch barrier. May load mixed versions or write protected state. | Stop further publication, retain observations, inspect affected state; no automatic rollback or acceptance. |
| Already-running process missed during drain | UNRESOLVED residual visibility/identification risk. | Explicit risk acknowledgement required before use; a discovered process invalidates readiness and triggers stop/review. |
| Cached Python modules | Verified exit of identified holders is TECHNICAL evidence for those processes only; unknown holders UNRESOLVED. | No assertion that FD enumeration alone proves absence of cached code; disclose limitations. |
| Retained file/directory descriptors | Identified-holder exit and reinspection are TECHNICAL observations; missed holders UNRESOLVED. | No claim that scheduler changes revoke descriptors. Stop on discovered activity. |
| Controller termination | TECHNICAL durable intent/progress and unchanged scheduler exclusion; manual exclusion remains PROCEDURAL. | Fresh independently observed recovery; no implied success or automatic continuation/release. |
| SSH disconnection | Same durable transaction/scheduler controls; responsibility continuity PROCEDURAL. | No timeout-based release. If responsibility cannot continue, stop and retain maintenance restrictions. |
| System reboot | Preserved scheduler bytes/exclusion require actual reinspection; processes/launcher state and operator readiness become UNKNOWN. | Invalidate readiness; stop mutation until fresh review/authorization. No guaranteed prevention of alternate boot launchers is claimed. |
| Unexpected cron modification | TECHNICAL digest/byte rechecks detect observed drift, not an adversarial compare-and-swap guarantee. Concurrent editor prevention PROCEDURAL. | Stop; preserve changed bytes and do not overwrite them with an assumed baseline. |
| Partial file publication | TECHNICAL per-file atomicity, recorded prefix/pending intent and exact observation. Entire set is not atomic. | Keep scheduler exclusion/no-launch restriction; pending uncertainty stops automatic adoption/retry/rollback. |
| Interrupted rollback | TECHNICAL recorded restored identities/pending intent; no supported automatic resume. | Keep maintenance restrictions; independent inspection and explicit disposition required. |

No complete event history or universal absence of transient execution is claimed.
Any actual unauthorized change remains subject to the original protected-state
judgment; accepting residual risk never makes that change authorized.

#### 5. One bounded maintenance-window procedure (specification, not commands)

1. Obtain explicit amendment adoption, later validated implementation acceptance,
   and a separate production authorization naming operator, pause scope, time
   window, residual risks, abort/recovery responsibility and release authority.
2. Establish exact source, runtime target/security/ancestor and scheduler baselines.
   Retain original scheduler bytes and identities privately with the existing
   transaction evidence; validate exact reconstruction before changing scheduling.
   No actual new production observation is invented by this specification.
3. Classify every relevant active scheduler entry as explicitly EXCLUDE or PRESERVE.
   Reuse the three established OPERATOR_SUPPLIED incident/inventory/platform lines;
   do not treat installer examples as production facts. Any other affected PE-4/
   PE-5 job requires exact identification and explicit pause approval. Preserve all
   unrelated bytes, comments, entries and services. Never stop system cron globally.
4. Under the named operator's exclusive scheduler-edit procedure, remove only the
   approved lines, verify exact expected maintenance bytes, and retain the original
   bytes plus both digests. Expected-state drift stops without overwriting it.
5. Identify known affected processes, interpreters, manual and persistent launchers;
   record inspection scope, visibility gaps, PID/start identities and evidence of
   completion or explicitly authorized stop. Do not kill by broad name/UID patterns.
   Recheck known processes and lock activity; no identified affected process may
   remain. Do not count a single empty process snapshot as future launch exclusion.
6. Establish the operator's no-manual-launch restriction and responsibility through
   interruption. Record acknowledgement of unknown callers/cached modules/retained
   descriptors. Unacknowledged risks or gaps preventing known-process validation
   block readiness. No permissions, identities, mounts or namespaces are changed.
7. In the adopted/validated future provider, run bounded preflight and prepare
   using UID/GID1000:1000. Preserve and verify five originals, stage/verify all13
   accepted source artifacts and retain the existing controller journal. Recheck
   source/target/ancestors, scheduler and known-consumer readiness before publication.
8. With separate exact commit authorization, publish dependencies first and incident
   engine last. Preserve durable intent->effect->verified installed identity and
   the existing journal. Drift or any failure stops without automatic repair.
9. Verify all13 actual installed hashes, ownership/modes and ancestor identities,
   expected untouched content and applicable protected observations. Record actual
   outcomes; COMMITTED alone does not prove success or authorize activation.
10. On controller/SSH interruption or reboot, retain scheduler exclusions and manual
    restriction. Reopen and validate original scheduler evidence, journal, backups,
    installed/restored prefix and all relevant actual filesystem observations.
    Re-establish known-process/window readiness. Pending/unconfirmed publication or
    interrupted rollback remains blocked for explicit disposition; no new resume
    API or automatic adoption is introduced.
11. If rollback is needed, obtain distinct authorization and use only a controller-
    accepted state with exact current identities and verified backups. Reverse the
    proven installed prefix; remove only proven new files. Verify full restoration.
12. Only after complete verified installation OR verified authorized rollback and
    fresh explicit release authorization, require the exact expected maintenance
    scheduler, restore original bytes and re-read/verify them. A failed restoration
    does not authorize manual release. Then explicitly end the no-launch restriction.
    No catch-up execution, monitoring, notifications, migration or PE-7.4 work follows.

A planned end time is a stop/escalation deadline, never permission to reopen an
uncertain runtime. If responsibility or recovery cannot safely continue, preserve
restrictions and obtain explicit disposition rather than silently extending authority.

#### 6. Observable production acceptance prerequisites

All must be evidenced before dependent production action; this proposal supplies none:

- Explicit amendment adoption and independent acceptance of the resulting Windows
  implementation, with unchanged original contract and all existing validation gates.
- Exact authorized HIOC pause/restore scope and named operator/responsibility transfer;
  explicit acknowledgement of independent/missed/cached/retained-caller residual risk.
- Verified original scheduler baseline and exact approved exclusion result; no
  unreviewed entries, concurrent edits or unrelated service/job changes.
- Bounded known-consumer inventory and actual drain evidence, including visibility
  limits; no known affected holder remains and no unsupported universal claim.
- Exact accepted source and target paths/hashes/modes/owners/ancestors; successful
  source/runtime preflight; backups/stages verified and actual restore readiness.
- Durable transaction evidence and an explicit abort/recovery contact/procedure,
  including pending-publication, interrupted-rollback, SSH-loss and reboot stop rules.
- No unexpected impact on Pi-hole, Unbound, NUT or unrelated services. Planned HIOC
  missed cycles/pauses are authorized; snapshot-age/freshness policy remains unchanged.
- Actual post-install/rollback identities and applicable original protected evidence;
  no inference from journal labels alone. Independent review and fresh release
  authority precede restoration. Original HA/UI/trust delivery and later P/A matrix
  obligations remain separately gated; this 13-file step does not close all PE-7.3.

#### 7. Minimum implementation/test changes ONLY IF subsequently approved

Preserve accepted controller transaction core, filesystem/descriptor handling,
manifest, journal structural/provenance validation and fresh-process recovery.
Add a narrowly scoped maintenance-window consumer provider and bounded scheduler/
process observations. Express the approved mixed technical/procedural assurance
honestly in the existing maintenance evidence, with exact authorizations, scheduler
bindings, known-process observations, limitations and residual-risk acknowledgement.
Necessary closed-schema/provider/recovery validation changes must be explicit,
phase-specific and confined to that adopted assurance; no blanket gate override,
operator-boolean bypass or historical test relaxation. Existing mode0000 synthetic
fixtures remain preserved historical tests, not evidence of the amended mechanism.

Add focused tests for exact scheduler preservation/exclusion/restoration and drift;
known-process drain failure; missing/expired/window/recovery authorizations;
unacknowledged risks; controller/SSH interruption and reboot invalidation; partial
publication and interrupted rollback refusal; no automatic release; fresh recovery;
UID1000 access and no permission/namespace/broker changes. Assert that procedural
manual restrictions are never reported as complete technical exclusion. Run the
appropriate native/source validation only after a separately authorized code change.

No code is changed now. Native refusal gates must remain until explicit adoption,
authorized implementation/validation and separate production authority. No current
controller invocation is made deployable by this document.

#### 8. Explicit decision required and relationship to prior proposals

The operator may approve or reject this complete amendment wording and its stated
assurance reduction. Approval must explicitly accept the independent/missed/cached/
retained-caller risks for the later specified maintenance scope; it is not implied
by asking for this proposal. Adoption is distinct from implementation authorization,
production execution, rollback and consumer release authorization.

Experimental broker remains UNADOPTED. Root-only quarantine/private mount-namespace
architecture remains UNADOPTED. No new prototype, framework, background service,
identity, privilege or production mechanism is introduced. Earlier experiments,
reviews and accepted controller/broker tests are preserved without repetition.

Exactly one next action: operator approval or rejection of this amendment proposal.
PE73_MAINTENANCE_WINDOW_AMENDMENT=PROPOSED_NOT_ADOPTED.
PE73_PRODUCTION_DELIVERY_AUTHORIZED=FALSE; PE74_STATUS=NOT_AUTHORIZED.
STOP_REQUIRED=TRUE.


### PE-7.3 approved maintenance-window amendment adoption — 2026-10-23

Classification: CURRENT ADOPTED IMPLEMENTATION-LEVEL DECISION.
PE73_MAINTENANCE_WINDOW_AMENDMENT=ADOPTED_OPERATOR_APPROVED.
Authority: explicit operator request "Adopt Approved Maintenance-Window Amendment
and Implement Guarded Native Coordination", supplied attachment
8e20e365-1502-4042-99c5-475991d15ae7, 2026-10-23. This authorizes bounded Windows
implementation/validation and this adoption, NOT native execution or production.

Superseded only for the amended maintenance-window path: the implementation-level
complete independent-caller exclusion prerequisite quoted at lines812-818 and its
corresponding later readiness assertions. Their exact historical text and synthetic
fence tests remain intact. The proposal at line2357 is retained as proposal history;
its prior NOT_ADOPTED label is superseded by this explicit decision. No historical
receipt or production fact is rewritten. No original PE-7 contractual requirement
is superseded, including exact security identities, protected evidence and separate
installation/activation/rollback/release authority.

The approved reduction is explicit: identified scheduled-launch exclusion is
technical; known-process draining is observed and limited; manual-command control
is procedural. A missed/cached/retained/noncooperating independent caller remains
residual risk. Adoption is not universal exclusion, authenticated native permission,
acceptance of an unauthorized change, native qualification or production authority.
The exact wording below matches the previously reported proposal byte-for-byte
as UTF-8 text (without the surrounding code fences):

~~~text
During a separately authorized PE-7.3 maintenance window, publication and rollback
may use the existing UID-1000 controller only after exact approved scheduled
launches have been excluded and reobserved, known affected processes have been
identified and verifiably drained, and one named operator has accepted exclusive
maintenance responsibility and prohibited independent/manual affected commands.
Scheduled-launch exclusion is a verified technical control over the identified
scheduler entries. Manual-command restrictions are procedural controls, not
technically enforced exclusion. Draining covers the identified processes and
observed evidence only; it does not prove universal absence of cached modules,
retained descriptors, undiscovered processes or alternate launchers.

The authorization must explicitly acknowledge the residual risk of a
noncooperating independent caller or an affected process missed during drain.
This amendment does not claim complete consumer exclusion. It does not authorize
unexpected writes, mixed-version execution, service impact or acceptance without
the original mandatory evidence. Unresolved visibility limits and residual risks
must be stated; documentation alone does not accept them.

Exact scheduler preservation, source/target/security checks, all 13 artifact pins,
backups, dependency order, durable controller intent and verified progress,
independent filesystem inspection, and separately authorized rollback remain
mandatory. Controller failure, SSH loss, window expiry, pending publication or
interrupted rollback must never trigger automatic retry, adoption, rollback,
scheduler restoration or consumer release. The operator's no-launch restriction
continues until explicitly released. Reboot invalidates the maintenance readiness
assessment and requires fresh scheduler/process/runtime inspection before any
further mutation; no crash-persistent universal execution boundary is claimed.

Scheduler restoration and procedural consumer release require fully verified
installation or fully verified authorized rollback, exact current-state checks
and a fresh explicit release authorization. Unexpected scheduler modification,
known consumer activity, identity drift or insufficient mandatory evidence stops
dependent work without overwriting unreviewed state. The controller journal alone
never proves filesystem success, scheduler enforcement, process drain or safe
release. All other accepted PE-7 requirements remain unchanged.
~~~

Broker and root-only quarantine/mount-namespace proposals remain UNADOPTED.
PE-7.1/7.2 COMPLETE/PASS; PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
Native commit/rollback/scheduler changes remain blocked pending separately
accepted native qualification and separate production execution authorization.


#### Guarded maintenance-window repository provider and validation

PE73_MAINTENANCE_WINDOW_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC.
NATIVE_WINDOW_ACCEPTANCE=NOT_ESTABLISHED; PRODUCTION_AUTHORIZED=FALSE.
This PASS concerns Windows implementation/validation only. Native qualification,
production execution, scheduler mutation, rollback and release remain unavailable.
No PI3/PI5/HA/MQTT/credential/production access or runtime execution occurred.

New bounded files: tools/pe73_maintenance_window.py and
 tests/test_pe73_maintenance_window.py. No existing controller/test/broker file changed.
WindowController inherits the accepted prepare/commit/rollback/verify algorithms;
small wrappers add native preparation and evidence-bound runtime authorization gates.
Its extended closed journal uses one explicit window member in the SAME journal.json.
A read-only in-memory projection invokes the unchanged strict Controller._journal
validator for every core field, installed/restored prefix, source digest, snapshot
and backup provenance. Projection is validation only: no alternative on-disk journal
or competing installation authority. The new envelope independently validates its
closed shape, phase/core relationship, ordered unique authorization references,
original/reduced scheduler hashes, preserved bytes, observations and release binding.
Old synthetic maintenance and new window envelopes cannot be mixed. The old CLI
continues to refuse native consumer coordination and cannot adopt the new envelope.

The accepted artifact algorithms, five backups/eight new targets, ordered atomic
publication, exact ownership/modes/ancestor checks, descriptor lifecycle and
pending-effect refusal remain unchanged. Broker still pins the unchanged accepted
controller. The previously accepted104 controller tests remain byte-identical.

NativeOps implements fixed-argv read-only crontab and bounded /proc observations,
with PID start identity checked around command reads. Receipts expose command
hashes and bounded PID/limitation codes, not raw private command arguments. Known
active consumers or incomplete inspection refuse drain; the provider never kills
processes or assumes that command/FD inspection proves cached-module absence.
Unknown processes and cached/retained-reader limits are disclosed as limitations.
This classifier is not universally complete and has NOT been qualified on PI3.

Scheduler preservation uses private verified window-crontab-original evidence under
the existing transaction. Exact maintenance_cron inventory rules preserve unrelated
bytes and exclude only approved lines. Scheduler effects use one fixed crontab
installation attempt with before/after byte checks; this is not a native CAS or
proof against an independent scheduler editor. Intent is persisted before each
scheduler effect, and failed/uncertain effects cannot be retried automatically.

NativeOps.live_gate unconditionally raises NATIVE_WINDOW_ACCEPTANCE_REQUIRED;
NativeOps.scheduler_gate unconditionally raises NATIVE_SCHEDULER_NOT_QUALIFIED.
Both guard the native scheduler effect path; live_gate also guards preparation,
maintenance progression, runtime authorization, publication and rollback. No CLI,
boolean, receipt or environment setting unlocks native execution. The actual fixed-
argv mutation seam exists behind those guards for later explicit qualification;
Windows tests use isolated synthetic Ops, never production operations. No native
qualification capability or operator deployment command is issued here.

Grants bind exact action/reference, full extended-journal digest, current scheduler
digest, named operator, instance session, boot identity, bounded expiry, explicit
exclusive responsibility and exact residual-risk acknowledgement. This is a closed
procedural authorization input, NOT a claim of cryptographically authenticated
operator identity or a production permission simply because a dict can be supplied.
The eventual authorized native runner/operator-evidence provenance remains a native
acceptance prerequisite. Runtime commit/rollback each need their separate matching
single-use instance grant; core transaction references remain durable provenance.

No context exit, timeout, exception or successful install restores cron or releases
manual restrictions. Reopening a provider invalidates its instance readiness. ATTACH
requires exact original scheduler/scope, secured backup, strict journal and actual
runtime comparison, then invalidates old drain evidence and records the fresh boot/
session. A fresh DRAIN and current operator authorization are required before further
mutation. Reboot invalidates readiness. Pending publication, interrupted rollback,
uncertain scheduler effects and unexpected drift remain blocked; no resume/adoption
or repair API has been added. Actual process state is observed separately from
journal state. The operator identity cannot silently change on attachment.

Release requires complete installed or rolled-back core state with no pending
operation, actual matching runtime, source identity verification, fresh known-process
observations, exact scheduler expectation and a separate release authorization.
Original cron restoration is verified before the procedural restriction is marked
released. A restore failure stays RESTORE_UNCERTAIN; duplicate restoration/release
and automatic reopening are refused. Independent/manual exclusion is always
PROCEDURAL_ONLY; universal_exclusion=false in observations and receipts.

Final Windows validation used the established bundled Python stdin harness at the
repository root, -B, UTF-8, shell-free PATH, HIOC_TEST_SHELL cleared, and
sys.path[:0]=['tests','pi4/lib']. Results are recorded directly from unittest:

- Accepted controller regression:104 run,104 passed,0 failures/errors/skips.
- Final new provider module:35 run,35 passed,0 failures/errors/skips/class-level skips.
- Earlier combined run:136 run,136 passed (104 existing+32 new),344.125 seconds.
  Three final new cases and preparation/native-seam guards followed; the final35
  rerun took61.094 seconds and bound final source hashes. The unchanged controller
  regression does not import/depend on the new provider, so its104 result remains
  applicable. Do not count overlapping new cases as additional distinct coverage.
- Initial development-only run stopped at a test fixture boot ID shorter than the
  existing authorization-token grammar; the fixture was corrected, not the validator.
- Native scheduler calls in tests are mocked; process parsing uses a synthetic
  Windows /proc tree. No native behavior is claimed from these fixtures.
- Full historical HIOC suite and accepted broker54 tests were not repeated: runtime
  source, accepted controller/test and broker/test dependencies remain unchanged.

Final source hashes:

- tools/pe73_maintenance_window.py SHA256 cd571ee743894066276227cb7dcf2de46e3699de9ef4eeb7339350b9abab2093.
- tests/test_pe73_maintenance_window.py SHA256 628de43d2dd13fa0ce91c09547958ff24f57802c0c153e81d275b139f38219a6.
- tools/hioc-pe73-pi3-delivery.py SHA256 0589cf6363626d14ab9abe08c001ddef634b243326513b27de43a7b93aa4f95f.
- tests/test_pe73_pi3_delivery.py SHA256 4fef3799a3bae5733056fa30b3423bca656026103a6ce02e443e14ac639ce281.

Direct receipts retained outside the repository: hioc-pe73-window-result.json and
hioc-pe73-window-final-result.json in the Windows temporary directory. Failure detail
lists are empty; test source bytes were unchanged during their respective runs.

Focused checks cover inventory, exact preservation/exclusion/restoration, unrelated
entries, scheduler conflict/uncertainty, active/incomplete process observations,
authorization/risk/boot/session/expiry checks, stale recovery and mandatory re-drain,
interrupted publication/rollback, source/target drift, ordered authorization history,
strict core rejection, explicit release, duplicate operations, truthful manual limits,
fixed native argv, sanitized process identities and native preparation/mutation gates.

Preservation: all13 accepted delivery identities,39 successor identities and449
protected identities verified; original contract and accepted PE-7.1/7.2 artifacts
unchanged. Only the two necessary existing documentation identity entries are
refreshed. Current candidate adds only the two new window files; no unrelated path,
staging, commit or push. git diff --check passes; stash unchanged.

Remaining native prerequisites: independently accepted Windows candidate; separately
authorized fixed scheduler-effect qualification (including drift/uncertainty), actual
bounded process visibility/classification and PID-race behavior, operator-evidence
provenance and responsibility, boot/restart readiness, exact pause/restore approval,
backup/restore readiness, no collateral service impact and independent native
acceptance. Production commit/rollback remain unavailable until that separate native
acceptance and separate production execution authorization. No power-loss or
universal independent-caller exclusion claim is made.

Exactly one next action: concise independent acceptance of this Windows maintenance-
window provider candidate and its retained native gates, inside PE-7.3.
PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED; STOP_REQUIRED=TRUE.


### PE-7.3 relative-invocation process-detection correction

Classification: HISTORICAL ACCEPTED REPOSITORY CORRECTION, published in302a4e3f34f53fffb8299771d31c115e052b5400.
The current uncommitted checkout-compatibility correction is recorded below.
PE73_RELATIVE_PROCESS_FOCUSED_RECHECK=ACCEPT_FOR_NATIVE_QUALIFICATION.
The focused review verified the retained55/55 maintenance test evidence and active native refusal gates.
Native qualification remains incomplete; production delivery and rollback remain blocked.
PE73_RELATIVE_PROCESS_DETECTION_CORRECTION=PASS_REPOSITORY_SYNTHETIC.
The prior focused independent review returned PE73_MAINTENANCE_WINDOW_ACCEPTANCE=REJECT.
This correction resolves its confirmed known-relative-caller detection defect; the correction
itself did not grant independent acceptance, native qualification or production authority.
The subsequent focused independent review accepted this correction for native qualification only.

Confirmed original reproduction: cwd=/home/jazofv1/hioc/pi4/bin;
argv=python3 hioc-assets.py list. The pre-correction scanner produced known_active=[]
and inspection_complete=true, recorded the PID as unclassified and admitted drain.
The added test_original_relative_asset_invocation_blocks_actual_drain was executed
against the unchanged pre-correction provider and failed: expected Failure was not
raised (1 run,1 failure,0 errors). Thus this is a demonstrated detection correction,
not a new universal-exclusion requirement or a hypothetical production observation.

Exact correction in tools/pe73_maintenance_window.py:

- Fixed source-observed ENTRY_NAMES/ENTRY_PATHS identify existing HIOC Python CLI
  entry points. They are an inspection inventory, not claimed active production jobs.
- invocation parses NUL-delimited argv without shell evaluation. It identifies the
  script after CPython flags, warning/-X/hash-policy option arguments and '--';
  distinguishes -c code and -m module invocation; and does not interpret ordinary
  script arguments as additional launched scripts. Known hioc module invocation
  remains an affected import. Ambiguous option parsing cannot hide a potential
  known entry point.
- Potential known relative invocations require two observed /proc/PID/cwd readlink
  values. cwd_target uses POSIX pathname rules, never executes a script and never
  writes a path. Known canonical runtime-bin destinations are classified active.
  Missing/unreadable/deleted/changed cwd, lexical '..', unresolved aliases and a
  potential known name outside the verified canonical scope fail closed as incomplete
  classification rather than proving either affected or unrelated execution.
- PID directory device/inode and process start ticks bracket command/cwd inspection;
  command bytes are reread and cwd reread for potential relative invocations. Identity,
  argv or cwd changes mark inspection incomplete. A potential known process exiting
  during inspection requires a fresh scan before drain can be established.
- WindowConsumers._processes admission is unchanged: known_active or incomplete
  inspection refuses drain. Tests exercise this actual gate, not parser labels only.
  Unrelated Python commands are not classified affected merely for being Python or
  mentioning a filename in an ordinary argument. Unknown callers/cached modules and
  retained descriptors remain explicit limitations; universal_exclusion=false and
  manual_launch_control=PROCEDURAL_ONLY remain unchanged.

Regression coverage includes original relative invocation, absolute invocation,
'./hioc-assets.py', classification CLI, direct script argv, interpreter flags and
option arguments, hioc module invocation, unrelated commands, no shell evaluation,
missing/unreadable cwd, changed start/cwd/argv, process exit, ambiguous script/option
resolution and empty valid scans. Every classification outcome that matters to
readiness is checked through actual _processes drain admission. The native parser
uses isolated Windows synthetic /proc files and mocked cwd reads, never PI3 evidence.

Validation: established bundled Windows Python stdin harness, repository root, -B,
UTF-8, shell-free PATH, HIOC_TEST_SHELL cleared, sys.path[:0]=['tests','pi4/lib'].
Final focused module:55 run,55 passed,0 failures,0 errors,0 skips,0 class-level skips.
Harness elapsed60.266 seconds; direct result/source hashes and empty failure details
are retained in temporary hioc-pe73-relative-correction-result.json. The intentional
pre-correction failing regression remains historical evidence. An intermediate
source import syntax error was corrected before this complete successful final run.
Final source bytes were unchanged during validation.

- tools/pe73_maintenance_window.py SHA256 c16e031121ca0cb450e30822f0711c1cc19f4d1757d6664c4d2c383b78b03dc5.
- tests/test_pe73_maintenance_window.py SHA256 b94fb1fe0740b330929532861209227255ae496d8b8407bac4b2443cdb758541.

The accepted104 controller tests were NOT rerun: their source and dependency/interface
set are unchanged and they do not import the corrected provider. The prior104/104
result remains historical accepted evidence. No historical HIOC or broker suite was
repeated. Original core journal/artifact transaction authority, descriptor handling,
accepted controller/test files, broker/test files and the original contract remain
unchanged. No production module or13-artifact manifest was modified.

The adopted amendment remains verbatim SHA256
b57c6f0a67aa90ff24fd42a454bc2822a7652ba03aff1f72a4c7be336d570127.
Native live_gate and scheduler_gate still unconditionally raise
NATIVE_WINDOW_ACCEPTANCE_REQUIRED and NATIVE_SCHEDULER_NOT_QUALIFIED respectively.
No flag, environment, receipt, journal or privilege bypass was added. No production
maintenance/delivery or native qualification is authorized by this correction.

Preservation verification:13 delivery identities,39 successor identities and449
protected identities; accepted controller/broker/contract identities; exact amendment
text; native refusals; no unexpected path and git diff --check. Only corresponding
two existing documentation identity entries are refreshed. Candidate still has3
modified tracked files,6 authorized untracked files,0 staged/unexpected paths and
unchanged stash. No PI3/PI5/HA/MQTT/credential/production access, cron/permission/
service/runtime mutation, deployment, rollback, activation, stage, commit or push.

Historical progression before publication: controlled publication of the accepted nine-file candidate,
followed by separately authorized operator-run PI3 release-source synchronization.
This publication does not authorize native maintenance, delivery, rollback or PE-7.4.
PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED; STOP_REQUIRED=TRUE.


### PE-7.3 exact release-source checkout compatibility correction

Classification: HISTORICAL VALIDATED INTERIM CORRECTION, 2026-10-23.
Superseded by the publication-stable identity correction below. The two-HEAD model
and its 221-test result are retained as historical evidence, not current authority.
PE73_SOURCE_CHECKOUT_COMPATIBILITY=PASS_REPOSITORY_SYNTHETIC.
The prior nine-path qualification candidate was published at
302a4e3f34f53fffb8299771d31c115e052b5400. OPERATOR_SUPPLIED PI3 evidence reports
release-source HEAD at that exact commit, controller RELEASE at
51398bab4e2293b578b2cdac2d0740c3738cab2f, SOURCE_GATE_MATCH=False and no production
mutation. These are supplied observations, not Codex production access or proof of
native qualification. The previous gate equated checkout HEAD with payload release.

RELEASE remains the immutable 13-artifact payload revision 51398bab4e2293b578b2cdac2d0740c3738cab2f.
QUALIFICATION_CHECKOUT names exactly 302a4e3f34f53fffb8299771d31c115e052b5400.
source_gate accepts only those two exact HEAD identities: the original payload
checkout retains existing historical test compatibility; the qualification checkout
is explicitly authorized. No ancestor, branch-name or arbitrary-newer-commit rule
was introduced. A future correction publication commit is NOT implicitly admitted.
All 13 payload reads and Git-blob checks still use RELEASE:path, never checkout HEAD.
Expected origin, clean tracked/untracked tree, exact repository root, subprocess
isolation and filesystem security requirements are unchanged. SOURCE is unchanged.
MANIFEST, PRIOR, ORDER, MODES and transaction payload release fields are unchanged.

The maintenance provider's PIN is refreshed to the corrected controller's exact
SHA-256: . The experimental broker also had an exact controller dependency pin; ONLY
that constant is refreshed so its synthetic fixture loader does not reject this
authorized source correction. Its architecture, limitations, experimental/unadopted
status and lack of native privilege/integration authority are unchanged.

Focused regressions accept the exact qualification checkout and original payload
checkout; reject unauthorized/random/intermediate revisions, dirty tracked and
untracked trees, wrong root/origin and each of 13 payload byte/blob mismatches;
verify 13 immutable object reads and 13 immutable blob checks; and verify the
provider's exact pin and pre-import refusal of a mismatched controller.

Validation used the established bundled native Windows Python stdin harness,
repository root, -B, UTF-8, shell-free PATH including WindowsPowerShell/v1.0,
HIOC_TEST_SHELL cleared and sys.path[:0]=['tests','pi4/lib']. Complete affected
controller module: 110 run, 110 passed. Maintenance-window module: 57 run, 57 passed.
Affected experimental broker module: 54 run, 54 passed. Total: 221 run, 221 passed,
0 failures,0 errors,0 skipped,0 class-level skips. All six source/test identities
were unchanged during validation. Earlier 104/55/54 accepted results and historical
correction evidence remain preserved; no unrelated historical suite was rerun.

Controller old SHA-256: 0589cf6363626d14ab9abe08c001ddef634b243326513b27de43a7b93aa4f95f.
Controller new SHA-256: b1a33af96e894df1400d8dec715abba1e5f6265ea8c27f83eb92b07ef81b10d8.
Maintenance provider old SHA-256: c16e031121ca0cb450e30822f0711c1cc19f4d1757d6664c4d2c383b78b03dc5.
Maintenance provider new SHA-256: 183e06c75299ea32414b85bed29b23a8a6c35c800250de25f38cf4a469e26fe6.
Experimental broker old SHA-256: b7db2f55dd99fb1e7161a3afc054695bb5151b3866618dc8e2267afc0da47469.
Experimental broker new SHA-256: 632c70d6f97b64a42d14ffde2901a6c8d8ebf49e5593db27bd32367b13a6e214.
Controller tests SHA-256: 4a40901f3a262c6302dcffca76ba74a69e3c22fe16c3fc0fc0beed72d9519bb7.
Maintenance tests SHA-256: e48da1831398f8a9ce76a3fa175068f6504b7c94d51190460bc7d9dfa7455508.
Broker tests unchanged SHA-256: 3ee70a530e8b4b9e87ffed1fff4f56948b33e0abdccb22812ba2135b279bc791.

Static verification: 13 delivery identities, 39 successor identities and 449 protected
identities PASS; original PE-7 contract and approved amendment verbatim unchanged.
Only the two documentation entries in the existing successor record are refreshed.
Native live_gate and scheduler_gate retain unconditional
NATIVE_WINDOW_ACCEPTANCE_REQUIRED and NATIVE_SCHEDULER_NOT_QUALIFIED refusals.
Native commit/scheduler modification/rollback/release remain blocked. No deployment,
maintenance, production execution, runtime modification, staging, commit or push
was performed; Codex accessed neither PI3 nor PI5. The operator evidence was not
recast as native qualification completion or comprehensive consumer exclusion.

PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED; NATIVE_QUALIFICATION=INCOMPLETE.
CORRECTION_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED; CORRECTION_PUBLICATION=NOT_PERFORMED.
Exactly one next action: independent acceptance of the exact uncommitted correction
and its identities before separate publication authorization. STOP_REQUIRED=TRUE.


### PE-7.3 publication-stable source-integrity correction

Classification: CURRENT UNCOMMITTED WINDOWS REPOSITORY CORRECTION, 2026-10-26.
PE73_PUBLICATION_STABLE_SOURCE_IDENTITY=PASS_REPOSITORY_SYNTHETIC.
The initial Windows baseline was main at 302a4e3f34f53fffb8299771d31c115e052b5400,
equal to origin/main, with the expected eight modified tracked paths, empty staging,
zero untracked paths and unchanged stash. The complete existing candidate was
preserved. No HIOC repository reset, stash, staging, commit or push was performed.

Root cause: the original gate equated checkout HEAD with payload release. The first
uncommitted correction allowed only the payload and one qualification HEAD. Its
221 passing tests established those cases but did not solve publication: publishing
the corrected tool necessarily creates another HEAD that the finite list rejects.
That interim model and validation remain historical above; they are superseded here.

The three identities and their authority are now separate:

- PAYLOAD: RELEASE remains 51398bab4e2293b578b2cdac2d0740c3738cab2f. All 13 artifacts
  are read from RELEASE:path and checked against the unchanged accepted SHA-256 and
  Git blob pins. MANIFEST, SOURCE, PRIOR, ORDER, MODES, destination layout, journal
  payload release, publication order and rollback contract are unchanged.
- TOOLING: the provider still compares the controller's exact source SHA-256 before
  importing it. That one-way consistency pin is refreshed only because source_gate
  changed. The broker's dependent constant is also refreshed; the broker remains
  experimental and unadopted. Final controller and provider hashes below are identity
  measurements for independent acceptance, NOT independent approval. A mutable
  repository hash, matching internal pin, receipt, branch or boolean cannot itself
  authenticate operator approval or authorize production mutation. Native tooling
  qualification still requires separately accepted external operator authorization
  and evidence; this task implements no automatic approval/trust mechanism.
- REPOSITORY: source_gate verifies an actual HEAD commit object, exact source root,
  exact expected origin URL and clean tracked/untracked status. It verifies the
  immutable payload commit, then requires RELEASE to be an ancestor of HEAD using
  Git with --no-replace-objects. This relationship preserves the accepted payload
  foundation while allowing qualification publications on its history. It is source
  integrity only, not approval of the intervening commits or of their tooling. A
  missing payload, unrelated history, dirty tree, wrong root/origin or wrong payload
  digest/blob is refused. Fixed Git argv/environment, read-only commands and all
  filesystem-security checks are preserved. No current or future qualification HEAD
  is hardcoded or predicted, and no HEAD-relative payload file read was introduced.

Publishing another tooling/evidence commit on that history does not require a code
edit to recognize its SHA. Its tooling still needs independent source-identity
acceptance. Repository integrity may pass for an unapproved controller revision;
the unchanged provider pin detects unexpected controller bytes, and integrity does
not unlock either native gate. No claim is made that the same mutable repository can
authenticate its own approval or that arbitrary unapproved Python is safe to execute.

Integration validation used isolated temporary local clones with --no-hardlinks;
no shared object-store corruption or production/network operation was performed.
Git computed commit objects, roots, status, ancestry and payload object reads. The
test transport only adapts the fixed Linux Git executable/environment to Windows.
It does not fabricate Git answers. Tests covered the original payload checkout,
the published qualification checkout, and two successive real disposable commits
containing the corrected controller/provider without another source or allowlist
edit. They rejected dirty tracked/untracked state, wrong root/origin, missing payload
commit, corrupted fixture blob, unrelated HEAD even with payload objects present,
wrong payload SHA/blob pins and unexpected controller bytes in a clean descendant.
The actual provider and controller were loaded together; valid source integrity
still refused native prepare/commit/rollback, maintenance progression/release,
runtime authorization and scheduler installation. No NativeOps gate was overridden.
Separate explicitly synthetic state also verified journal payload/closed-field and
maintenance-window authorization boundaries. Existing relative-process detection,
recovery, partial-failure, rollback and release tests remain in effect.

The initial focused attempt ran 9 tests: 8 passed and 1 failed at the exact root gate
because a temporary Windows short-path alias differed from Git's canonical root.
The fixture now obtains Git's canonical path and proves samefile identity before
using it. No production path check was normalized, relaxed or bypassed. The failed
run is retained separately; it was not rewritten as success. After that fixture-only
correction the focused 20 tests passed, including all 12 real-Git integration cases.

Final validation used the established bundled native Windows Python stdin/runner
harness, repository-root cwd, -B, UTF-8, shell-free PATH including WindowsPowerShell,
HIOC_TEST_SHELL cleared and sys.path[:0]=['tests','pi4/lib']. Focused20 passed, then
the remaining 159 controller/provider and 54 affected broker tests passed. The final
accepted run set has 233 distinct test IDs with no duplicated cases across phases:
controller 110/110, maintenance-window 69/69, experimental broker 54/54; 0 failures,
0 errors,0 skips,0 class-level skips. All six validated source/test byte identities
were unchanged during these runs. No full historical HIOC suite was rerun.

Final measured SHA-256 identities (not independent authorization):

- tests/test_pe73_filesystem_broker_prototype.py: `3ee70a530e8b4b9e87ffed1fff4f56948b33e0abdccb22812ba2135b279bc791`.
- tests/test_pe73_maintenance_window.py: `1750da615fe13f7c337db54e5b4459e2eb32989a0123bb952ff0ad57bd4ebc66`.
- tests/test_pe73_pi3_delivery.py: `eab315647b37ec45f9ee1ca65766f7f0e96535db0bfaffdd6e64e01fdea0e63b`.
- tools/hioc-pe73-pi3-delivery.py: `76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2`.
- tools/pe73_filesystem_broker_prototype.py: `baed2cf58feaf683ba9530b517600ff9b97faf25ba25920662bf0f2840565d3a`.
- tools/pe73_maintenance_window.py: `beb11380bd0aef0aaa465521731e315c0e8d1621261b1c2caea1d14efb31dc6f`.

Static preservation: all 13 immutable delivery identities, 39 successor identities
and 449 protected identities PASS. The authoritative original PE-7 contract and the
approved maintenance-window amendment remain byte-for-byte unchanged. Only the two
necessary documentation SHA/Git-blob entries in the existing successor record are
refreshed; unrelated governance identities and acceptance history remain unchanged.
The controller delta is confined to source integrity, and the provider/broker code
deltas are their exact controller pins. No transaction or maintenance architecture
was rewritten. CRLF-aware Git whitespace checks and documentation references pass.

NATIVE_WINDOW_ACCEPTANCE_REQUIRED and NATIVE_SCHEDULER_NOT_QUALIFIED remain
unconditional. No configuration, environment, JSON receipt, approval boolean,
checkout or test override can bypass these actual native gates. Native qualification
is incomplete; no production delivery, scheduler change, rollback or release is
enabled. No PI3/PI5 access, production observation/mutation, deployment, classification,
producer execution, runtime/cron/permission/service change or PE-7 activation occurred.
Temporary test Git commits are disposable fixture evidence only, not HIOC publication.

PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED; NATIVE_QUALIFICATION=INCOMPLETE.
CORRECTION_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED; CORRECTION_PUBLICATION=NOT_PERFORMED.
Exactly one next action: independent acceptance of the exact uncommitted
publication-stable source-identity correction before separate publication authority.
STOP_REQUIRED=TRUE.


### PE-7.3 bounded native coordinator implementation — 2026-10-26

PE73_NATIVE_EXECUTION_IMPLEMENTATION=PARTIAL.
Authority: Complete Bounded Native Maintenance-Window Execution, supplied attachment
d8240a21-9c5a-43a3-b053-3925fe672677. Windows implementation and focused validation
only; staging, publication and all production operations are unauthorized.
Baseline: clean main and origin/main at85c1a4f1f270c48ef9b00efe55eae759265303ab.

The operator supplied source-integrity PASS, verified five replacement/eight absent
new targets, native scheduler/process observation PASS and in-memory cron reduction
PASS. These are OPERATOR_SUPPLIED, not Codex production observations. Original cron
SHA2563f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9;
reduced SHA256443485cfb47920db8d6263e5266eb9f68811e81c06390a983a7006aac581b930.
Twelve active entries: exactly three excluded, nine preserved. The supplied five
infrastructure jobs and four additional HIOC-related jobs have no demonstrated
dependency requiring exclusion. No new dependency is asserted. Storage approximately
4029 MiB is operator-supplied evidence, not a fresh capacity guarantee.
The earlier consolidated assessment caught a different dynamically loaded Failure
class; neither native gate is changed to accommodate that assessment error.

Implementation: MaintenanceCoordinator in tools/pe73_maintenance_window.py binds
WindowConsumers and its inherited WindowController without duplicating publication,
rollback, backup, journal or security algorithms. Its native constructor uses the
existing target identity, NativeFS and exact source_gate; it checks both approved
cron digests and an explicit complete inventory, with only the known three exclusions.
The read-only context includes actual13 target snapshots (security and ancestors),
fresh source/payload validation, exact scheduler, process identities/completeness,
boot, session, journal, inventory and requested action. Per-action input must name
the operator, external reference, complete context digest, expiry, exclusive manual
responsibility and all six accepted residual risks. A context-bound authorization
digest is retained as the existing durable authorization reference; the window's
existing grant hash/order/uniqueness rules remain. Hashes bind supplied decisions,
not authenticate their provenance. They cannot unlock native qualification.

The coordinator supports explicit PREPARE, PRESERVE, EXCLUDE, DRAIN, ESTABLISH,
COMMIT, ROLLBACK, ATTACH, AUTHORIZE_RELEASE, RESTORE_SCHEDULER and RELEASE through
the existing methods. Every operation refreshes context; runtime publication still
rechecks readiness and actual filesystem provenance. Manual launch control stays
PROCEDURAL_ONLY; universal exclusion is false. No generic enabling CLI, environment
variable, acceptance receipt loader, privileged mechanism, process killing or
automatic recovery is introduced. No runtime engine is executed.

The existing scheduler operation compares exact expected bytes, attempts only one
fixed /usr/bin/crontab - installation with bounded timeout/sanitized environment,
and rereads exact installed bytes. EXCLUSION_UNCERTAIN/RESTORE_UNCERTAIN is durable
before the command. Error, timeout, lost acknowledgment or bad readback leaves an
uncertain phase without retry, restoration or release. Proven interrupted artifact
prefixes require fresh attachment/drain and separately authorized rollback; pending
or unverifiable publication/rollback refuses adoption. Restart requires fresh
session attachment and drain; reboot invalidates old readiness. Release requires
actual complete installation or verified rollback, then separate release,
restoration and procedural-release authorizations. Controller/SSH failure and
window expiry do not restore cron.

Validation:19 new real-controller/provider/coordinator integration tests PASS plus
69 affected provider/process/parser/identity/real-Git tests PASS:88 run,88 passed,
zero failures/errors/skips/class-level skips. The new tests use real Windows fixture
bytes and the actual fixed scheduler read/install functions against a synthetic
subprocess endpoint; native authority and POSIX metadata are explicit stand-ins.
They cover complete13-file publication, preserved unrelated entries, five restored
replacements/eight removed new files, process visibility/active refusal, source and
runtime drift, invalid/expired authorization, interrupted publication/rollback,
restart/reboot, scheduler drift, timeout, lost acknowledgment, bad readback and
native-gate refusal. No live crontab command is launched. Both executable source
hashes were identical before/after each valid run. The initial sandbox attempt
stopped at fixture setup/cleanup permissions (one test, two environment errors);
its report is preserved separately. The same harness then passed with escalation.
The unchanged controller110 and broker54 historical tests are retained evidence,
not rerun. No full historical suite was run.

Current provider SHA256:7fe35ddaae5d182e5a23f545253cc7cdcddaadde0127a9b06d76e142f511dba8
Current provider-test SHA256:6024f29daaec23e9009164473a08c16e571eab06b9c10f3659b0ed011fc84721
Controller SHA256 remains76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2.
Static verification:13 immutable delivery identities,39 successor identities and
449 protected identities PASS; original contract, amendment, core controller,
experimental broker and all unrelated tracked files unchanged. Only two existing
document identity entries are refreshed in the successor record. Git diff/check,
empty index, baseline HEAD/origin/main and unchanged stash are verified.

Remaining native requirement / bounded qualification disposition:
NATIVE_WINDOW_ACCEPTANCE_REQUIRED and NATIVE_SCHEDULER_NOT_QUALIFIED remain
unconditional. No matching authorization, publication identity or Windows test can
bypass either. Consequently this is a PARTIAL implementation, not a completed or
production-capable native execution claim. The fixed scheduler command installs
the invoking UID1000 user's live table; no alternate isolated scheduler target is
established by existing PI3 evidence. A mocked command, read-only inventory or
syntax check cannot qualify real installation, single-attempt uncertainty handling
and exact restoration. No safe contained PI3 installation command can therefore
be supplied under the prohibition on changing that live table merely for testing.

One consolidated qualification requirement, requiring separate authorization:
provide an isolated non-production Linux scheduler target with no live HIOC jobs;
exercise the same fixed bounded install/readback operation against an exact saved
table, a three-entry-reduced table with all unrelated entries preserved, and exact
restoration; capture return codes/readback/uncertainty without retries or touching
the PI3 live table. Its target/isolation is currently NOT_ESTABLISHED. This is the
smallest remaining scheduler evidence requirement, not a new architecture or
permission to create an account, use sudo, alter scheduling or deploy. No operator
mutation command is issued in this candidate. Native window acceptance and later
execution authorization still remain separately necessary.

Exactly one next action: obtain separate authorization and a defined isolated
non-production Linux scheduler target for that bounded qualification.
PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED; BROKER=EXPERIMENTAL_UNADOPTED.
CODEX_PI3_ACCESS=FALSE; CODEX_PI5_ACCESS=FALSE; PRODUCTION_MUTATED=FALSE.
STAGING_PERFORMED=FALSE; COMMIT_CREATED=FALSE; PUSH_PERFORMED=FALSE.


### PE-7.3 native deployment readiness — 2026-10-26

PE73_DEPLOYMENT_READINESS=READY_FOR_OPERATOR_AUTHORIZATION.
Authority: Finish Native Deployment Readiness, supplied attachment
e8bd7a64-9d97-478d-86be-bfa437481298. This supersedes the immediately preceding
PARTIAL readiness disposition only. Earlier unavailable-environment findings,
unconditional-gate descriptions, test failures and the five-file candidate are
preserved as historical evidence. No contract/amendment or production record changes.
Baseline main/origin/main85c1a4f1f270c48ef9b00efe55eae759265303ab, exact prior five
unstaged paths, empty index, no untracked paths and unchanged stash were verified.

#### Real native qualification (local, non-production)

An already installed Ubuntu24.04 WSL2 environment was discovered on the Windows
host. It is JorgePC, UID/GID1000:1000 (jazofv1), Python3.12.3, with an existing real
/usr/bin/crontab. Its current-user crontab was exactly absent: exit1, empty stdout,
exact C-locale absence message. /home/jazofv1/hioc was absent. No Docker/Podman
executable was found; no infrastructure, host software or persistent service was
created. The initial sandbox WSL listing denial was resolved through read-only
escalation, not treated as proof that Linux was unavailable.

The isolated qualification installed a UUID-bound fixture containing a comment and
four nonexecuting February31 /usr/bin/true entries, reduced it by exactly three
entries using the actual provider NativeOps.install_scheduler operation, then
restored the exact fixture. Each native operation was single-attempt and exact
readback matched. After successful verification only, the exact fixture was
removed once and absence was verified. No unrelated schedule was overwritten.
Only target/qualification admission was specialized to the explicitly identified
non-production WSL account; scheduler observation/install code and all subprocesses
were real. There were no mocks, scheduler API substitutions or automatic recovery.
Three total install attempts: fixture creation, reduction, restoration; one exact
fixture-removal attempt. The accepted native operation fingerprint is:
8c7026ba84b748677381ea9adfef9334156795eabb16df059a2e752a90049e66.
It binds the exact source of NativeOps.scheduler and NativeOps.install_scheduler,
including fixed argv, timeout, environment, expected-state comparison and readback.
Native scheduler admission checks that fingerprint; changing those functions
invalidates qualification. No mutable qualification receipt can unlock the guard.

Exact local scheduler qualification receipt (CODEX_OBSERVED_LOCAL, not PI3):
```json
{
  "after": "EXACTLY_ABSENT",
  "before": "EXACTLY_ABSENT",
  "crontab_sha256": "d71b4e26034ec955cae7e7101a4b33f5923b3396a0e1e1893cd1274bbb51c3ec",
  "fixture_cleanup": "EXACT_FIXTURE_REMOVED",
  "fixture_remove_attempts": 1,
  "fixture_sha256": "898ed40da0ba08117894db11b70d8884bfa31ba39cec12f1d370bf0968d6f360",
  "gid": 1000,
  "host": "JorgePC",
  "install_attempts": 3,
  "kernel": "6.18.54.1-microsoft-standard-WSL2",
  "mocks": false,
  "pi3_access": false,
  "pi5_access": false,
  "production_access": false,
  "python": "3.12.3",
  "qualified_at_unix": 1793042123,
  "real_subprocesses": true,
  "reduced_sha256": "b8fb7dc17927e2488a1ef6f14c87a8b60f8b57e7fa6a47db393dc147a9661b2d",
  "restore_attempts": 1,
  "result": "PASS_ISOLATED_REAL_LINUX_SCHEDULER",
  "retry_performed": false,
  "scheduler_operation_sha256": "8c7026ba84b748677381ea9adfef9334156795eabb16df059a2e752a90049e66",
  "service_created": false,
  "software_installed": false,
  "target": "LOCAL_NON_PRODUCTION_WSL_UBUNTU_24_04",
  "uid": 1000,
  "unrelated_table_overwritten": false
}
```

A separate contained Linux pseudo-terminal exercised the actual tty_line function
with /dev/tty, not stdin. Bounded prompt/read and child exit0 PASS. The actual
NativeOps constructor refused the WSL host with TARGET_IDENTITY. No scheduler or
repository file changed in that check. Exact receipt:
```json
{
  "child_exit_status": 0,
  "controlling_tty_read_write": true,
  "files_modified_in_repository": false,
  "native_target_refusal_on_wsl": true,
  "production_access": false,
  "result": "PASS_REAL_LINUX_CONTROLLING_TTY",
  "scheduler_modified": false,
  "target": "LOCAL_NON_PRODUCTION_WSL",
  "tty_function_sha256": "949f035f2beaaa76b448b96e8e2408ec791fef39251cd94a114df1f15ebafc7f"
}
```

These results qualify the fixed Linux operation, not a PI3 execution, universal
Linux/crontab compatibility, production health or consumer exclusion. PI3's exact
scheduler and all source/runtime identities are still rechecked before mutation;
unconfirmed native exit/readback remains uncertain and cannot be retried.

#### Native execution/authorization completed

The existing NativeOps, MaintenanceCoordinator, WindowConsumers and inherited
WindowController remain the only execution path; the core controller is unchanged.
NativeOps.live_gate now requires an internal, ephemeral admission created only after
the controlling-terminal confirmation of an exact operation-specific digest.
The prompt binds action, external authorization reference, UID1000_jazofv1,
five-minute expiry, exact context and all six residual risks. The actual target is
rechecked as Linux nutandpihole with real/effective UID/GID1000, current process and
boot identity, wall expiry and monotonic deadline. A matching input dict, persisted
journal, environment variable or command-line flag cannot create admission.
Authority is forgotten in finally; cron restoration, rollback and release are never
performed by finally. The manual no-launch commitment is procedural, not technical.

Scheduler admission additionally requires the current action to be EXCLUDE or
RESTORE_SCHEDULER, the exact qualified operation, the corresponding durable
EXCLUSION_UNCERTAIN or RESTORE_UNCERTAIN journal phase, matching session/boot,
latest action/reference and an unused one-attempt admission. Native receipts state
the isolated Linux scheduler qualification scope explicitly, and distinguish
CURRENT_OPERATION_ONLY authorization from any standing production permission.

The interactive runner acquires the exact already-reviewed original/reduced cron
and12-entry inventory (three exclusions/nine preserved), reads immutable13 payload
objects, validates real targets and presents one action at a time. It does not
automatically advance, retry, kill processes, alter services, run an engine, deploy
HA, migrate Assets, or activate PE-7. Every operation needs a new typed exact digest.
The original legacy controller CLI still refuses unsupported consumer coordination;
the amended path does not weaken or bypass it. Broker remains experimental/unadopted.

#### Validation and preservation

Final Windows native harness:18 native-admission integration tests PASS plus88
affected controller/provider/coordinator/real-Git tests PASS:106 run,106 passed,
zero failures/errors/skips/class-level skips. The native-admission tests exercise
the real admission/interactive/coordinator guards with explicitly synthetic target,
process, TTY and scheduler endpoint observations; they are not native production
evidence. Complete13-artifact installation and separately authorized rollback,
independent filesystem verification, scheduler restoration/release, invalid identity,
process activity, stale/mismatched authority, reboot, scheduler drift, interrupted
publication and failed restoration are covered. Real Linux scheduler and tty checks
above provide the actual OS-operation evidence separately. No unrelated historical
suite was rerun. The unchanged controller110 and broker54 evidence remains retained.

Two development attempts are preserved, not counted as passing validation: the
first stopped at3 run/2 passed/1 error because the literal seven-character username
did not satisfy the existing eight-character authorization identifier minimum.
The runner now uses UID1000_jazofv1; the validator is unchanged. The next attempt
stopped at16 run/15 passed/1 fixture failure: its tty-denial test accidentally called
the already mocked tty reader. The test now calls the saved real reader with explicit
Windows substitutes for POSIX open flags. No production gate was weakened for it.
Final executable hashes were unchanged before/after both successful Windows runs.

Provider SHA256:9f363fb6fbdc1a40ccd0e8d150c18a7340c8f40565647c182d63af68487db920
Provider tests SHA256:8de66c13e1e0a8ec33c09c92b1784622717d79f2a24aed63fcee9cb641eaffe9
Controller remains76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2.
Static checks verify13 immutable delivery identities,39 successor identities and
449 protected identities; original contract and verbatim amendment unchanged.
Only the two existing document identity entries are refreshed in the successor
record. Five total unstaged paths, empty index, zero untracked paths, unchanged
HEAD/origin/main85c1a4f1 and stash, diff/check PASS. No publication performed.

#### Deferred deployment runbook — PI3 NUT&PIHOLE

This runbook is PREPARED, NOT AUTHORIZED TO EXECUTE. First obtain controlled
publication authorization and publish these accepted bytes; then separately
authorize operator-run source synchronization and the bounded production window.
Codex must not access PI3/PI5. No runtime copy, scheduler mutation or PE-7 execution
is authorized by this Windows assignment. The command below only applies after
the corrected, hash-matching candidate is published and synchronized.

Preflight: operate as jazofv1 on nutandpihole. Preserve the approved manual no-launch
restriction and exclusive operator responsibility. Check that the synchronized
release-source is clean and contains these exact tool bytes. The runner itself
rechecks host/UID/GID, root/origin/ancestry/cleanliness,13 immutable source objects,
target security/provenance, exact original/reduced scheduler and fresh process state.
Do not resolve a failure by changing schedules, hashes, permissions or scope.

Prepared operator launch command (not authorized now):
```sh
/usr/bin/python3 -I -S -B - <<'PY'
import hashlib, pathlib, runpy, stat
root = pathlib.Path('/home/jazofv1/hioc-release-source')
expected = {
    'tools/hioc-pe73-pi3-delivery.py': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2',
    'tools/pe73_maintenance_window.py': '9f363fb6fbdc1a40ccd0e8d150c18a7340c8f40565647c182d63af68487db920',
}
for relative, digest in expected.items():
    path = root / relative
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        print('RESULT=FAIL_STOP_TOOLING_IDENTITY')
        raise SystemExit(1)
runpy.run_path(str(root / 'tools/pe73_maintenance_window.py'), run_name='__main__')
PY
```
Immediately capture the process status in the same SSH shell:
```sh
PE73_EXIT_STATUS=$?
printf 'PE73_EXIT_STATUS=%s\n' "$PE73_EXIT_STATUS"
```

Execution: enter one action and a unique external authorization reference at each
prompt. References use8-96 ASCII letters/digits/underscore/hyphen. Inspect the full
context/risk prompt and type only the exact freshly displayed AUTHORIZE line when
that operation is separately authorized. Do not prefeed or replay confirmations.
The intended normal sequence is PREPARE, PRESERVE, EXCLUDE, DRAIN, ESTABLISH, COMMIT,
AUTHORIZE_RELEASE, RESTORE_SCHEDULER, RELEASE. Each action needs its own reference
and exact confirmation. PREPARE durably backs up five originals and stages13 payloads;
PRESERVE saves exact cron before EXCLUDE; COMMIT publishes dependency-first with
the shared incident executable last. Verification reads actual filesystem state,
not only journal labels. STOP abandons the session without restoring/releasing.

Verification: preserve each sanitized operation receipt and exit status. Require
COMMITTED/pending-null and actual installed identity matches for all13 targets;
then obtain separate release authorization. Require exact original cron readback
after RESTORE_SCHEDULER and final RELEASED evidence. This delivers inactive artifacts
only; it does not authorize monitoring, notifications, Asset migration or PE-7.4.
Existing cron consumers can resume only after verified completion or authorized
rollback under the accepted manual-window assurance model.

Recovery: any FAIL_STOP, timeout, SSH loss, unexpected process, scheduler edit,
identity drift or uncertain effect ends dependent work. Preserve journal/backups
and the manual no-launch restriction. Do not retry, re-run cron installation,
automatically restore, or infer release from expiry. A fresh runner after restart
or reboot requires a separately authorized ATTACH and fresh DRAIN before further
consequential operations; it does not advance/adopt partial state. ROLLBACK requires
its own authorization and exact installed/baseline provenance. Pending publication,
interrupted rollback, PRESERVATION_UNCERTAIN, EXCLUSION_UNCERTAIN or RESTORE_UNCERTAIN
cannot be automatically adopted or retried; stop for explicit evidence disposition.
Only fully verified installation or verified authorized rollback can authorize
scheduler restoration and final procedural release. No force/repair override exists.

Exactly one next action: obtain controlled publication authorization for this
validated five-file candidate. No immediate PI3 action is authorized.
PE73_STATUS=IN_PROGRESS; PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED.
CODEX_PI3_ACCESS=FALSE; CODEX_PI5_ACCESS=FALSE; PRODUCTION_DEPLOYMENT_PERFORMED=FALSE.
STAGING_PERFORMED=FALSE; COMMIT_CREATED=FALSE; PUSH_PERFORMED=FALSE.


### PE-7.3 simple operator interface — 2026-10-26

PE73_SIMPLE_OPERATOR_INTERFACE=PASS; UNATTENDED_DEPLOYMENT_SUPPORTED=FALSE.
Authority: Eliminate Manual Cryptographic Deployment Confirmations. This changes
only the operator interface of the candidate published at43b3084948831e45ccfb0e4bac2f2394d97ea631.
That published source remains the verified clean baseline. The prior manual ACTION /
EXTERNAL_REFERENCE and hash-copying procedure is historical and superseded by this
section for the corrected candidate; all original decisions/evidence remain intact.

The predefined normal sequence is PREPARE -> PRESERVE -> EXCLUDE -> DRAIN ->
ESTABLISH -> COMMIT -> AUTHORIZE_RELEASE -> RESTORE_SCHEDULER -> RELEASE. Native
bootstrap, exact source/root/origin/ancestry/cleanliness, runtime security/provenance,
scheduler, process and context checks run automatically. The operator is never asked
to select an action, supply a reference, read JSON, or copy a digest. Each interactive
operation generates an AUTO_action_UUID reference and its existing exact context /
authorization hash internally. Fresh context is verified before/after the response;
NativeOps still requires the same ephemeral operation-specific admission.

Every one of the nine journaled steps retains separate human authorization. The
existing grant-order contract includes preservation, drain/readiness and independent
release/restoration; these are not silently converted to unattended permissions.
Only read-only/internal checks advance without a new decision. Separately requested
rollback/attachment still use their own operation-specific approval and existing
recovery gates, and are absent from the predefined normal sequence. No blanket
approval, environment/CLI switch or receipt/journal override is introduced.

The controlling terminal accepts only Y or N, case-insensitively, after trimming
leading/trailing whitespace. Only Y authorizes the displayed step. Blank, N, YES,
mixed/multiple answers or other input stops before that operation's effects.
tty_line flushes queued/type-ahead terminal input before displaying every prompt;
an answer pasted for a preceding operation cannot authorize the next operation.
The existing bounded tty read, terminal type check and descriptor cleanup remain.
Human impact/restriction text replaces prompt JSON/digests; sanitized technical
receipts are still emitted after each completed step for later review, explicitly
labelled as requiring no interpretation for the next decision.

Fresh source/runtime/scheduler/process/journal, boot/session/expiry, named operator,
exclusive responsibility and all six residual risks remain bound internally.
Durable EXCLUSION_UNCERTAIN/RESTORE_UNCERTAIN intent, qualified native scheduler
operation fingerprint, one attempt and exact readback are unchanged. N, failure,
SSH interruption or expiry never retries, rolls back, restores cron or releases
callers. The manual no-launch restriction remains until explicit release; it is
procedural and does not claim universal exclusion. Existing pending/uncertain
transaction refusal, separate rollback and fresh recovery requirements remain.

Validation:26 focused tests PASS (18 adapted native-admission integration tests,
eight added operator-interface tests), zero failures/errors/skips/class-level skips.
These exercise the actual fixed sequence/coordinator/provider/controller with explicit
Windows OS/TTY/scheduler fixtures, including whitespace Y across real transaction
steps, nine unique internal references/context bindings, exact13-file installation,
separate release/restoration, invalid/mixed/blank responses, wrong operation,
technical drift, refusal/interruption after exclusion, fresh-context/reboot/expiry,
failed restoration and refusal to auto-resume an existing transaction. No production
execution is inferred. Source hashes were unchanged across validation.
The prior88 affected transaction/source/process tests are retained rather than
rerun: their relevant algorithms and test ASTs remain unchanged. Existing106-run
published evidence remains historical; it is not relabelled as this correction's run.
The core controller, NativeOps live/scheduler guards, source gate, window algorithms,
grant validator, journal semantics and native scheduler implementation are unchanged.

Real local non-production Linux pseudo-terminal test PASS: an initial whitespace Y
was accepted, an additionally queued N was flushed before the second prompt, and a
new separately entered whitespace Y was required. No scheduler, service, permission,
credential, runtime or repository source mutation occurred in that test. The native
crontab operation is unchanged and retains its already recorded real Linux
qualification; it was not reinstalled merely for this interface correction.
Exact new tty qualification receipt (CODEX_OBSERVED_LOCAL, not PI3):
```json
{
  "child_exit_status": 0,
  "files_modified_in_repository": false,
  "production_access": false,
  "queued_old_response_discarded": true,
  "result": "PASS_REAL_LINUX_SIMPLE_YN_TTY",
  "scheduler_modified": false,
  "separate_fresh_responses_required": true,
  "target": "LOCAL_NON_PRODUCTION_WSL",
  "tty_function_sha256": "360c41a3d04c3e6ff6330b5f7afd5130bab5a07a602b8a2001be94abf80dbb06",
  "whitespace_y_accepted": true
}
```

Provider SHA256:3df4790ca50fb2f67c91f09140c8d248d7f78fd6ff40f464bed2e3afe34b921c
Provider tests SHA256:bd26c3d203b2a95db912a427a06aa4b23c78d5167c6c65b5a6425dd1ddb981f3
Controller unchanged:76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2.
All13 immutable delivery,39 successor and449 protected identities verify. Only two
existing document identity entries are refreshed. Original contract and verbatim
approved amendment remain unchanged; experimental broker remains unadopted. Five
unstaged files only; index empty, no untracked paths, stash unchanged; main and
origin/main remain43b3084948831e45ccfb0e4bac2f2394d97ea631, ahead/behind0/0.

#### Corrected complete operator command — PI3 NUT&PIHOLE

PREPARED ONLY. This uncommitted correction must first be separately published and
the exact corrected tools synchronized to release-source. Separate production
authorization is still required. The currently published old runner fails the new
hash check; do not bypass that check or copy runtime files manually.
The operator copies this complete command; no digest/reference must be typed or
manually validated. Hashes are enforced internally. No interactive-shell set -e,
sudo, SSH logout or automatic recovery command is used.

```sh
/usr/bin/python3 -I -S -B - <<'PY'
import hashlib, os, pathlib, runpy, socket, stat, sys
if (sys.platform != 'linux' or socket.gethostname() != 'nutandpihole'
        or not os.getuid() == os.geteuid() == os.getgid() == os.getegid() == 1000):
    print('RESULT=FAIL_STOP_TARGET_IDENTITY')
    raise SystemExit(1)
root = pathlib.Path('/home/jazofv1/hioc-release-source')
expected = {
    'tools/hioc-pe73-pi3-delivery.py': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2',
    'tools/pe73_maintenance_window.py': '3df4790ca50fb2f67c91f09140c8d248d7f78fd6ff40f464bed2e3afe34b921c',
}
for relative, digest in expected.items():
    path = root / relative
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or hashlib.sha256(path.read_bytes()).hexdigest() != digest):
        print('RESULT=FAIL_STOP_TOOLING_IDENTITY')
        raise SystemExit(1)
print('PI3 NUT&PIHOLE: each step requires its own Y/N decision. No step is approved by starting this command.', flush=True)
runpy.run_path(str(root / 'tools/pe73_maintenance_window.py'), run_name='__main__')
PY
PE73_EXIT_STATUS=$?
printf 'PE73_EXIT_STATUS=%s\n' "$PE73_EXIT_STATUS"
```

The immediate exit-status capture is included at the end of the command. The
runner reads decisions from /dev/tty, not the here-document or a prefilled input file.

Exact common notice before each approval:
```text
PI3 NUT&PIHOLE - operator jazofv1. Approve this step only.
You must control this window alone. Do not run independent or manual affected commands until release is confirmed.
A known process may be missed; cached modules, retained file descriptors, alternate launchers and concurrent schedule edits remain risks. Manual restrictions are procedural, not universal technical exclusion.
N, blank or invalid input stops. Stopping never automatically retries, rolls back, restores the schedule or releases callers. Keep the manual restriction until explicit release.
```
Each step then displays its exact impact text, followed by exactly:
```text
Approve this step? [Y/N]:
```
The nine impact texts, in order:

1. Save five original files and prepare thirteen verified delivery files. No live runtime file is replaced.
2. Save the exact current schedule for later verified restoration. Scheduled jobs are not changed.
3. Temporarily pause the three approved HIOC scheduled jobs. Preserve the other nine entries.
4. Check that no known affected process is running and record the observation. Do not stop or kill processes.
5. Recheck the schedule and known processes, then record that this maintenance window is ready.
6. Install the thirteen verified files in dependency order and verify them. Do not activate PE-7 features.
7. Authorize reopening only after the complete installation or authorized rollback has been verified. This step does not restore the schedule.
8. Restore and verify the exact original schedule. The three paused HIOC jobs can run again.
9. Finish the verified window and end the restriction on independent or manual affected commands.

Permitted responses: Y approves only that displayed step; N refuses it and stops.
Leading/trailing spaces/tabs and lowercase y/n are accepted. Blank is never approval.
Do not paste a list of answers; queued responses are discarded. Starting the command
does not approve any operation. There is no supported no-further-approvals mode.
After refusal/interruption, keep the manual restriction; do not restart the normal
sequence as recovery. Preserve output/journal and obtain the existing separately
authorized recovery disposition. The source/production and PE-7.4 boundaries remain.

STAGING_PERFORMED=FALSE; COMMIT_CREATED=FALSE; PUSH_PERFORMED=FALSE.
CODEX_PI3_ACCESS=FALSE; CODEX_PI5_ACCESS=FALSE; PRODUCTION_DEPLOYMENT_PERFORMED=FALSE.
PE73_STATUS=IN_PROGRESS; PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED.


### PE-7.3 approved-process resume and material-context correction — 2026-10-27

PE73_APPROVED_PROCESS_RESUME_IMPLEMENTATION=PASS_REPOSITORY_VALIDATION.
Production remains unobserved/unmodified by Codex. PE-7.3 IN_PROGRESS; PE-7.4
NOT_AUTHORIZED. This is the existing deployment correction, not another checkpoint.
Baseline main/origin/main1452534a23528af96e69b9ec030f050b61bed859 was verified clean.

#### Operator-supplied interrupted production state

EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED, not a Codex PI3 observation. The owner reports
source1452534a23528af96e69b9ec030f050b61bed859; transactionPREPARED, pendingNone,
windowEXCLUDED; scheduler443485cfb47920db8d6263e5266eb9f68811e81c06390a983a7006aac581b930;
original scheduler3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9;
journal file SHA256b899a8fa79bde3c6619d6abd8217d88833c414823e7888358ed7a043b766600f.
Three HIOC entries are excluded and nine unrelated entries preserved. No artifact
installation or rollback occurred. Last failure NATIVE_AUTHORIZATION_CONTEXT_DRIFT
during DRAIN is preserved; no claim of successful deployment/health is made.

#### Confirmed code defect and evidence limitation

MaintenanceCoordinator.context previously retained the entire process observation
except observed_at. Its limitations list contains UNCLASSIFIED_PID_* and
VANISHED_PID_* diagnostic entries. Exact before/after context equality therefore
treated unrelated process-list churn as an authorization change. Controlled tests
reproduce that false-drift mechanism while source/runtime/scheduler/journal/boot
and affected-process/completeness evidence remain unchanged.
The original production before/after context pair was not supplied; the exact
historical differing field/PID and sole runtime trigger remain UNKNOWN. Do not
reinterpret this code reproduction as a captured PI3 context diff.

The new process authority projection retains fresh observed_at validation, boot_id,
inspection_complete, universal_exclusion=false, and sorted exact pid/start_ticks/
command_sha256 for every known affected process. Diagnostic unrelated PID lists
remain in inspection receipts but are outside the equality binding. Incomplete,
unreadable or ambiguous classification still refuses; it is not silently declared
unrelated. Known activity, changed known identities, scheduler/journal/runtime/source
drift, scope changes and reboot still stop consequential work.

#### Explicit successor authorization decision

The project owner's executive instruction is preserved verbatim in the new focused
governance record governance/pe7/pe73-sequence-authorization.json:

> NEVER request separate authorization for consequential operations on a process that has been previous approved as a whole. Regardless of the reasoning, and no matter how you frame it. it is illogical and inefficient.

This is an explicit successor operational-authorization rule, not a claim that the
older per-step human approval contract already permitted unattended execution.
It supersedes only repeated human approval within an already approved fixed process,
including its conditional installation, restoration and release. Fresh internal
technical authorization/grants remain separately bound for each operation.
Original PE-7 contract bytes, the verbatim maintenance-window amendment, historical
approval records/receipts and their original meanings are unchanged. The closed
PE-7.1 candidate record/schema is not expanded or repurposed; its two current doc
identities are refreshed as before. The new record is evidence, never a runtime
permission receipt, environment switch or mutable authority input.

Whole-process authority is PE73_OWNER_SEQUENCE_AUTHORIZATION_20261027. Execution of
the previously approved normal process or this specifically approved known-state
resume needs no new Y/N prompt, operation name, reference, JSON interpretation or
cryptographic copying. One named UID1000_jazofv1 retains exclusive maintenance
responsibility and the manual no-launch commitment through verified release.
All six residual risks and the procedural-only exclusion limit remain. Unexpected
recovery, rollback or material scope change is OUTSIDE this process authority and
requires a new authorization; there is no automatic request/fallback to recovery.

#### Bounded implementation and recovery

The existing normal entry now uses the fixed nine-step process. A dedicated
resume_native_main entry permits only the exact approved PREPARED/EXCLUDED anchor.
It validates secure raw journal SHA256, strict old journal/history, pendingNone,
empty installed/restored maps, no commit/rollback authority, windowEXCLUDED/drainNone,
original/reduced cron hashes and inventory/operator, current actual13 baseline
target identities, all13 staged bytes and all five preserved backup bytes, and fresh
source/process evidence BEFORE ATTACH writes a new session into the old journal.
No second transaction, repeated PREPARE/PRESERVE/EXCLUDE, backup replacement, cron
re-exclusion, reset or cleanup is performed.

The fixed approved resume is ATTACH -> DRAIN -> ESTABLISH -> COMMIT ->
AUTHORIZE_RELEASE -> RESTORE_SCHEDULER -> RELEASE. ATTACH is the accepted provider's
existing mechanism, not a new journal interpretation. It revalidates actual state,
updates session/boot and clears drain readiness. Fresh-session/reboot recovery from
the exact supplied anchor uses new observations; a reboot mid-sequence invalidates
the existing scope. Once ATTACH changes the anchor, another invocation cannot
silently adopt a later phase under this known-state entry.

_ApprovedSequence is a bounded orchestration layer over the existing coordinator,
not a new transaction/deployment framework. It accepts no caller-provided action
list, grant, approval flag or permission receipt. Its entry, action list, payload/
controller/cron/inventory scope, session/boot, process ID and one-hour maximum scope
are fixed internally. Per-operation grants receive unique references, fresh context
and at most five minutes bounded by the overall scope deadline. Authorization is
not silently extended, and each native operation still uses _NativeAdmission and
the unchanged NativeOps guards. Normal process authority never includes rollback.

Before every operation, the last verified raw journal hash must match; actual
runtime state must still match the strict journal; source/scope/scheduler/process
checks run fresh. Context is revalidated by the unchanged execute technical gate.
After each operation, its reported canonical journal identity, actual state,
pendingNone, expected state/phase and filesystem inspection must match before the
next operation is admitted. Scope drift or any exception permanently stops that
in-memory sequence. Finally only forgets admission. It never retries, rolls back,
restores cron, releases callers or adopts uncertain evidence.

Existing dependency-ordered13-artifact publication, five-file backups, eight-new-file
provenance, fsync/readback, single-attempt scheduler installation with prior durable
uncertain intent, static verification and rollback algorithms remain byte/AST
identical. Legacy explicit-intervention tooling remains outside the approved normal
path; the normal/resume process never calls it or requests per-operation approval.

#### Focused validation and preservation

66 tests run,66 passed, zero failures/errors/skips/class-level skips:21 new approved
resume tests,26 adapted authorization/interface integration tests and19 existing
affected context/controller integration tests. The complete normal nine-step process
and exact fresh-session seven-step resume run without TTY calls. Real Windows
fixture bytes and actual provider/controller algorithms are used with explicit
synthetic native identity/process/scheduler sensors; this is not production evidence.
Tests cover exact anchor/phase, stages/backups before ATTACH, unchanged backup/stage
identities after completion, unrelated PID churn, known process appearance/identity,
incomplete observations, journal/runtime/source/scheduler drift, scope changes,
fresh reboot attachment, mid-sequence reboot, interrupted publication, one-attempt
restoration failure and refusal to replay/expand a stopped process. No actual PI3
journal or production fingerprints are reconstructed from assumptions.

The first attempt stopped at1 run/0 passed/1 fixture error because a helper named
sequence collided with an existing integer fixture counter. Its report is retained;
only the helper name was corrected. It is not counted as passing validation.
Executable hashes match before/after every successful run. Unaffected historical
controller/provider/source/broker suites were not rerun without source changes.
Native scheduler and tty functions are unchanged and retain their recorded real
Linux qualification. No new OS mechanism, broker, privilege or service is introduced.

Provider SHA256:756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741
Provider tests SHA256:a54a0ebaa4680ebf138ea76bd1bae8cab1a401782faee3ec8e4d14a96584c962
All13 immutable delivery,39 successor and449 protected identities verify; only two
current doc bindings change in the existing record. Original contract/amendment,
core controller, accepted window journal/publication/rollback algorithms, experimental
broker and unrelated files remain unchanged. Five tracked modifications plus the
one intended new successor record; empty index, unchanged stash, no other untracked
paths, main/origin/main1452534a, ahead/behind0/0. No staging/commit/push performed.

#### One prepared operator-run recovery command — PI3 NUT&PIHOLE

The code is an uncommitted Windows candidate. Corrected, hash-matching tooling must
first be available in the clean release-source checkout; the old1452534a provider
will refuse the new hash. No publication, source sync or production execution was
performed by Codex in this task. This is a code-availability prerequisite, not a
request for fresh approval of consequential operations inside the approved process.
The wrapper also requires the interrupted source1452534a in the corrected checkout's
ancestry. The immutable13 payload objects remain51398bab4e2293b578b2cdac2d0740c3738cab2f;
no circular future checkout hash or unrestricted release allowlist is introduced.

Copy this complete command only with corrected tooling available. It validates
the actual on-host state and either completes the exact approved continuation or
stops without inferring authority for a different recovery. It asks no Y/N questions.
Keep independent/manual affected commands prohibited until verified RELEASE.

```sh
/usr/bin/python3 -I -S -B - <<'PY'
import hashlib, importlib.util, json, os, pathlib, socket, stat, subprocess, sys
if (sys.platform != 'linux' or socket.gethostname() != 'nutandpihole'
        or not os.getuid() == os.geteuid() == os.getgid() == os.getegid() == 1000):
    print('RESULT=FAIL_STOP_TARGET_IDENTITY')
    raise SystemExit(1)
root = pathlib.Path('/home/jazofv1/hioc-release-source')
expected = {
    'tools/hioc-pe73-pi3-delivery.py': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2',
    'tools/pe73_maintenance_window.py': '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741',
}
for relative, digest in expected.items():
    path = root / relative
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or hashlib.sha256(path.read_bytes()).hexdigest() != digest):
        print('RESULT=FAIL_STOP_CORRECTED_TOOLING_NOT_AVAILABLE')
        raise SystemExit(1)
result = subprocess.run(
    ['/usr/bin/git', '--no-optional-locks', '--no-replace-objects',
     'merge-base', '--is-ancestor', '1452534a23528af96e69b9ec030f050b61bed859', 'HEAD'],
    cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    timeout=20, env={'PATH': '/usr/bin:/bin', 'HOME': '/home/jazofv1',
                     'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'GIT_OPTIONAL_LOCKS': '0'})
if result.returncode != 0:
    print('RESULT=FAIL_STOP_INTERRUPTED_SOURCE_ANCESTRY')
    raise SystemExit(1)
spec = importlib.util.spec_from_file_location('pe73_approved_resume', root / 'tools/pe73_maintenance_window.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print('PI3 NUT&PIHOLE: validating the exact approved interrupted window. No per-operation approvals will be requested.', flush=True)
try:
    status = module.resume_native_main()
except BaseException as error:
    code = error.code if isinstance(error, module.d.Failure) else 'RECOVERY_STOPPED_UNCERTAIN'
    print(json.dumps({'RESULT': 'FAIL_STOP', 'failure_code': code,
                      'automatic_recovery': False, 'consumer_release_implied': False,
                      'STOP_REQUIRED': True}, sort_keys=True), flush=True)
    raise SystemExit(1)
print('RESULT=PASS_APPROVED_EXCLUDED_RESUME')
print('PE73_STATUS=IN_PROGRESS')
print('PE74_STATUS=NOT_AUTHORIZED')
print('STOP_REQUIRED=TRUE')
raise SystemExit(status)
PY
PE73_RECOVERY_EXIT_STATUS=$?
printf 'PE73_RECOVERY_EXIT_STATUS=%s\n' "$PE73_RECOVERY_EXIT_STATUS"
```

Expected success: seven PASS_APPROVED_PROCESS_OPERATION receipts beginning ATTACH,
ending RELEASE, final PASS_APPROVED_EXCLUDED_RESUME and exit0. Capture all output.
Any mismatch/uncertainty produces FAIL_STOP/nonzero; do not rerun blindly, restore
cron, overwrite backups or choose another recovery automatically. Unexpected state,
rollback or changed scope requires the separate owner authorization already stated
above. This delivery process does not execute/activate PE-7 or authorize PE-7.4,
and successful installation alone does not close PE-7.3 governance acceptance.

CODEX_PI3_ACCESS=FALSE; CODEX_PI5_ACCESS=FALSE; CODEX_PRODUCTION_MUTATION=FALSE.
COMMIT_CREATED=FALSE; PUSH_PERFORMED=FALSE; PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED.


### PE-7.3 PI3 runtime deployment evidence and governance closure determination

Authority: owner-supplied deployment summary in the current closure request.
All PI3 production facts below are OPERATOR_SUPPLIED, not Codex observations.
No exact production observation date, raw receipt digest, new security metadata or
unreported execution result is invented. Accepted source publication is
`1c07932bd43aab1eac693ea07e195a74150fe550`; immutable payload remains
`51398bab4e2293b578b2cdac2d0740c3738cab2f`.

Reported interrupted-window recovery and deployment evidence:

- All 13 deployed artifact SHA-256 identities: PASS.
- Transaction COMMITTED, pending None; maintenance window RELEASED.
- Original 12-entry crontab restored exactly; all three affected HIOC jobs scheduled.
- cron, pihole-FTL, unbound and nut-server active.
- Incident-engine invocation and recent status output observed. Cron invocation is
  not proof of successful engine completion; no additional completion claim is made.
- Inventory last observed invocation 09:30, before maintenance release. No post-release
  inventory invocation or completion is claimed.
- Platform-status schedule daily 03:17; no invocation expected in the supplied
  post-release window. No post-release platform execution or completion is claimed.
- No HIOC error matches in inspected cron logs; independent post-deployment
  assessment reports zero failed invariants. Neither observation proves universal
  absence of errors or a comprehensive service-health/event-history audit.

The supplied evidence supports successful bounded PI3 runtime delivery, recovery,
scheduler restoration and release. It does not replace missing observations with
journal labels. Historical PREPARED/EXCLUDED state and the context-drift failure
remain preserved above; they are not the current supplied transaction state.
The controller, transaction/recovery algorithms, installed artifact pins, cron
specifications, original PE-7 contract and approved amendment are unchanged.

Manual-caller assurance remains procedural. Known-process draining and identified
scheduled-launch exclusion do not prove universal absence of independent/manual
callers, cached modules, retained descriptors, missed processes or alternate launchers.
This report does not authenticate unreported historical assurance observations or
waive the accepted residual-risk model. Executive instruction remains exactly:

> NEVER request separate authorization for consequential operations on a process that has been previous approved as a whole. Regardless of the reasoning, and no matter how you frame it. it is illogical and inefficient.

The unchanged `governance/pe7/pe73-sequence-authorization.json` preserves that decision
verbatim. One approved fixed process retains fresh technical checks; unexpected
recovery, rollback and material scope changes require new authorization. No automatic
retry, rollback, scheduler restoration or consumer release follows uncertainty.

**Closure determination: PE-7.3 remains IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.**
The original contract section13 PE-7.3 row requires guarded artifact/integration/UI/
trust delivery, exact paths/hashes/modes/owners/ancestors and observed HA API/resource
capability. Section7 requires supported live HA resource/Dashboard delivery with
export/backup; repository YAML copying is insufficient. The approved maintenance-
window preparation section6 expressly retains HA/UI/trust delivery and says the
13-file runtime step does not close all PE-7.3. The supplied production summary does
not establish those remaining delivery/capability facts; no violation or unsafe
operation is inferred from absent evidence. No new requirement or diagnostic phase
is introduced. Runtime deployment PASS is distinct from full checkpoint acceptance.
PE-7.4 P-matrix migration/operator edits/evaluation and actual UI behavior acceptance
remain later, separately gated; they are not demanded as PE-7.3 execution evidence.

Exactly one next action: separately authorize the remaining existing PE-7.3 guarded
HA integration/UI/trust delivery and required capability evidence, with adapter,
editing and evaluator disabled except explicitly authorized preflight. PE-7.4 is
not authorized. No production action is prepared or executed by this documentation task.

Publication is conditional on no unresolved mandatory acceptance criterion. That
condition is not met; these documentation/binding updates remain uncommitted and
unstaged. No commit or push is performed and no checkpoint closure is claimed.


### PE-7.3 integrated HA integration, UI and trust delivery preparation

Scope: authorized Windows-only implementation; baseline
`2784ef31da5e4ebc0e75af19695c8cc68c3d04a1`. The accepted PI3 deployment evidence
above and published sub-checkpoint are preserved. No PI3 deployment is reopened.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. No Codex PI3/PI5 access or production mutation.

**Result: PARTIAL for native delivery; integrated synthetic procedure PASS.**
The bounded implementation is `tools/pe73_ha_delivery.py`; read-only assessment is
`tools/pe73_ha_assess.py`; one consolidated test module is
`tests/test_pe73_ha_delivery.py`. Original PE-7.1 components are reused unchanged.
No new deployment framework, broker, privilege mechanism or credential system.

#### Exact artifact and publication boundary

All six inputs are read from immutable Git objects at
`51398bab4e2293b578b2cdac2d0740c3738cab2f`; SHA-256 AND Git blob pins are verified.
Under the ACTUAL observed HA configuration root, only these four live files may
be published, as UID/GID1000:1000, mode0644 under secure pinned ancestors:

- `custom_components/hioc_operator/__init__.py`
- `custom_components/hioc_operator/manifest.json`
- `custom_components/hioc_operator/services.yaml`
- `www/hioc-asset-editor.js`

The current NativeFS binding is limited to its already-supported UID/GID1000;
that is an implementation limit, NOT an observed PI5 identity. Other ownership is
a blocker; no sudo/chown/mode relaxation. Destination directories must already be
safely provisioned; the runner does not guess paths or create active configuration.
Foreign component files, duplicate editor cards, incompatible resource registrations,
unsupported layouts, dirty before-state and active HIOC services are refused.

The full `homeassistant/dashboards/hioc_dashboard_v2.yaml` and
`homeassistant/packages/hioc_incident_center.yaml` are verified/reference-backed,
NOT copied over the live Dashboard or package. They cannot silently enable existing
notification automations, change recipients/theme or replace unrelated HA behavior.

Private transaction `backups/pe73-ha-delivery-v1` is exclusively created, mode0700;
records/stages/backups mode0600. Existing transactions are never overwritten.
It preserves exact old file bytes and observed identities, stage bytes, complete
Dashboard/resource before-exports, both reference artifacts and
`trust.disabled.json`. These are private on-host records, not public Git evidence.
Descriptor-anchored no-follow reads, ACL checks, ownership/mode and bounded read
checks, fsync/replace and renameat2 no-replace for absent targets are reused from
the accepted NativeFS without altering the PI3 controller or its transaction.
Native POSIX/filesystem/ACL behavior for PI5 is NOT qualified by Windows fixtures.
Individual publication is atomic where the accepted primitives apply; four files,
HA API changes and the journal are NOT one globally atomic transaction.

#### Integrated sequence and supported HA mechanisms

`Delivery.run(plan, whole_process_reference=...)` performs one bounded approved
process, with no Y/N prompts. Source pins, actual host/capability/disabled guard,
trust checks, exact before-files, admin session, complete resource inventory and
observed Dashboard/view are required BEFORE any private transaction creation.
Qualified endpoints must establish exclusive delivery responsibility and stop
concurrent HA editing/configuration changes. Readback detects endpoint differences;
HA resource/config APIs provide no cross-request compare-and-swap or universal
consumer exclusion. No stronger race-free/transient-history assurance is claimed.

Prepare -> verified backups/stages -> four exact file publications -> supported
resource registration -> one additive editor card -> independent file/API readback.
Fresh guard/trust/journal/runtime/resource/Dashboard checks and a finite 15-minute
installation deadline remain mandatory. API calls are single-attempt. Durable
pending intent precedes each publication/API mutation; lost acknowledgement stops
with uncertainty retained. No automatic retry, rollback, restoration or consumer
release occurs after failure. A new session never auto-adopts a partial journal.

The API port uses the existing authenticated HA WebSocket request contract:
`auth/current_user`, `get_services`, `lovelace/info`, `lovelace/resources/list`,
`lovelace/config`, `lovelace/resources/create` (`res_type=module`, exact observed
`/local/hioc-asset-editor.js` mapping), and `lovelace/config/save` with the observed
`url_path`. No production URL, Dashboard/view ID or API support is invented.
The module supports an additive card in an observed masonry view, or an additive
grid section in an observed sections view, preserving all other config fields.
YAML-resource mode and unknown/panel/custom layouts stop rather than migrate.
No direct .storage edits; no resource reload, HA reload, restart or service call.

Primary-source API reference is HA core2026.8.1, matching the existing PE-7.1 HA
contract reference, not a claim of the installed PI5 version:
https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/lovelace/websocket.py
https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/lovelace/resources.py
https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/lovelace/const.py
Resource listing may lazily import a legacy resources section during initial load.
Therefore the synthetic native guard requires an already-loaded, established
resource collection. The assessment below does NOT call that API and cannot trigger
this migration. Its static source result is never substituted for live capability.

#### Trust preparation and disabled state

A closed disabled packet matches the existing integration Client fields and backend
adapter issuer-trust fields. It requires explicit HTTPS endpoint/address/port,
issuer/key ID, private certificate/key/CA/assertion-file references, a specific
operator allowlist and independent backend actor/operation/exact-Asset ACLs.
Wildcard permissions, missing ACLs, enabled entries and unknown extra fields fail.
No secret contents, production keys/certificates or defaults are generated/embedded.
The packet is a private offline preparation artifact, not installation into active
`configuration.yaml` or the PI3 adapter configuration. No credentials are provisioned.

Existing accepted Client/server_context/IssuerTrust behavior remains authoritative
for actual on-host private-file security, 32-byte assertion keys, certificate/key
consistency, client-SPKI pin and independent backend authorization. The live
`trust_preflight` port must bind those actual two-host observations and reject
missing/changed facts. A synthetic True, saved JSON claim or this evidence document
is not a native permission or proof of valid production trust.

Adapter/listener, editing services, observations, evaluator, migrations, recurring
PE-7 jobs and PE-7 notifications remain disabled. Tests actually invoke the unchanged
HA integration with all three role gates False and assert no clients/services/I/O.
No existing PI3 crontab, runtime, backups/journal or source is changed.

#### Recovery and limitations

Private file/API before-exports and pending journals survive interruption. An
uncertain/partial transaction requires explicit adjudication, never blind replay.
For a fully verified delivered-disabled transaction, explicit separate recovery
requires exact current live resource/Dashboard restoration through supported HA
management, verified against the saved exports, BEFORE file restoration. The
bounded `restore_files` then verifies installed identities and backup hashes,
restores old bytes/modes or removes only its proven new objects. It retains backups.
It does not restore old inode/timestamps, erase transaction history, automatically
roll back HA API state or change unrelated resources. A failed recovery also stops
with durable pending evidence. Rollback/material scope changes retain the unchanged
executive-decision boundaries; per-operation prompts are not reintroduced.

Native PARTIAL reasons are precise: actual PI5 root/owner/filesystem/API context
is not supplied; the existing authenticated connection and fresh host guard ports
have no production binding; actual two-host trust material is not inspected or
installed. The current tool is an integrated, callable synthetic candidate, not a
ready native CLI or evidence that HA/PI3 trust delivery has completed. No unqualified
native deployment command is offered. Backend packet preparation does not imply
PI3 trust installation. These requirements belong to the existing PE-7.3 scope.

#### Consolidated validation and exact candidate identities

One focused selection: test_pe73_ha_delivery, test_pe7_ha, test_pe7_security,
test_pe7_dashboard. Final result69 RUN/69 PASS/0 failures/0 errors/0 skipped;
class-level skips0. Includes real Windows temporary-file/fsync/replace fixtures,
existing local TLS fixture, and real Node editor assertions. No unrelated historical
suite or already-completed PI3 native qualification is repeated. All13 delivery,
39 successor,449 protected identities remain required and statically reverified
following documentation identity synchronization. Product source, controller,
maintenance provider, original contract and amendment remain byte-identical.

Two new fixture defects were corrected without changing accepted product code:
first8 run/7 passed/1 failure mocked Windows event-loop setup; second21 run/20
passed/1 error expected a Failure class from a different independent import, with
an event-loop mock diagnostic also observed. Both reports remain externally retained.
The final socket/client guards avoid modifying the socket class used by asyncio.

- `tools/pe73_ha_delivery.py`: SHA-256 `afb674da2bf781d4541defe61038addcfb4b0e22022156ed7a134a363a682bed`.
- `tools/pe73_ha_assess.py`: SHA-256 `5e01c99d484ee443e322621ba3262b77f02b1e4bc36a911aecb6aa78032498a1`.
- `tests/test_pe73_ha_delivery.py`: SHA-256 `a838cc41843fbe9da20a2aecf935048e0e24ff7a915635631af0af0f1c11c59c`.

#### One consolidated read-only PI5 assessment procedure

Run only as the operator in an existing PI5/HA execution environment. Enter the
actual config and installed `homeassistant` package directory, not guessed defaults.
Do not use sudo or install packages. If the host/container does not expose these
paths, return INSUFFICIENT_EVIDENCE; do not broaden diagnostics or mutate access.
The command reads only metadata and bounded public installed source. It does not
import/execute HA, read config/secret/.storage contents, call HA APIs, create files,
change ownership/permissions, reload or restart. Exit0 is assessment completed,
NOT native delivery readiness; source support alone never establishes live APIs.
Retain command arguments and full JSON as OPERATOR_SUPPLIED evidence.

~~~sh
printf 'Actual Home Assistant configuration directory: '
IFS= read -r PE73_HA_CONFIG
printf 'Actual installed homeassistant Python package directory: '
IFS= read -r PE73_HA_PACKAGE
python3 -I -S -B - "$PE73_HA_CONFIG" "$PE73_HA_PACKAGE" <<'PY'
"""One bounded read-only PI5 filesystem/source assessment. No HA imports/API calls.

Run with -I -S -B in the operator's existing Python, supplying the ACTUAL HA config
and installed homeassistant package directories. No guesses, credentials, .storage
contents, production configuration contents or state values are read or emitted.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def metadata(path):
    """No following symlinks, no implicit ownership correction."""
    for parent in (path, *path.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('SYMLINK_PATH')
    info = path.lstat()
    return {'device':info.st_dev, 'inode':info.st_ino, 'uid':info.st_uid, 'gid':info.st_gid,
            'mode':format(stat.S_IMODE(info.st_mode), '04o'), 'links':info.st_nlink,
            'type':'DIRECTORY' if stat.S_ISDIR(info.st_mode) else 'REGULAR' if stat.S_ISREG(info.st_mode) else 'OTHER',
            'mtime_ns':info.st_mtime_ns, 'ctime_ns':info.st_ctime_ns}


def assess(config, package):
    if not config.is_absolute() or not package.is_absolute() or '..' in config.parts or '..' in package.parts:
        raise ValueError('ABSOLUTE_OBSERVED_ROOTS_REQUIRED')
    result = {'RESULT':'READ_ONLY_ASSESSMENT', 'authority':'OPERATOR_SUPPLIED_WHEN_RETURNED',
              'uid':os.getuid() if hasattr(os,'getuid') else None,
              'gid':os.getgid() if hasattr(os,'getgid') else None,
              'host':__import__('socket').gethostname(), 'roots':{}, 'objects':{}, 'source_capabilities':{},
              'live_api_capabilities':'NOT_ESTABLISHED_BY_STATIC_SOURCE',
              'production_authorized':False, 'files_modified':False, 'STOP_REQUIRED':True}
    result['roots'] = {'config':metadata(config), 'package':metadata(package)}
    allowed = ('configuration.yaml','custom_components','custom_components/hioc_operator',
               'custom_components/hioc_operator/__init__.py','custom_components/hioc_operator/manifest.json',
               'custom_components/hioc_operator/services.yaml','www','www/hioc-asset-editor.js','backups',
               '.storage/lovelace',' .storage/lovelace_resources')
    for relative in allowed:
        relative = relative.strip()
        try:
            result['objects'][relative] = metadata(config/relative)
        except FileNotFoundError:
            result['objects'][relative] = {'exists':False}
    # Public installed source only; compile/AST inspection does not execute HA.
    for relative in ('components/lovelace/websocket.py','components/lovelace/resources.py',
                     'components/lovelace/__init__.py','components/frontend/__init__.py',
                     'components/websocket_api/connection.py','core.py'):
        target = package/relative
        info = metadata(target)
        if info['type'] != 'REGULAR' or info['links'] != 1:
            raise ValueError('UNSAFE_SOURCE_TYPE')
        with target.open('rb') as stream:
            raw = stream.read(2097153)
        if len(raw) > 2097152 or metadata(target) != info:
            raise ValueError('SOURCE_DRIFT_OR_LIMIT')
        tree = ast.parse(raw)
        names = {n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
        constants = {n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
        result['source_capabilities'][relative] = {'sha256':hashlib.sha256(raw).hexdigest(), 'metadata':info,
            'commands':[x for x in ('lovelace/config','lovelace/config/save','lovelace/info','lovelace/resources') if x in constants],
            'symbols':[x for x in ('current_connection','SupportsResponse','ResourceStorageCollection',
                'ResourceStorageCollectionWebsocket','websocket_lovelace_save_config') if x in names],
            'resource_load_may_import_legacy_configuration':relative.endswith('resources.py') and 'CONF_RESOURCES' in raw.decode()}
    return result


if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            raise ValueError('ACTUAL_CONFIG_AND_PACKAGE_DIRECTORIES_REQUIRED')
        receipt = assess(Path(sys.argv[1]), Path(sys.argv[2]))
    except BaseException as error:
        receipt = {'RESULT':'INSUFFICIENT_EVIDENCE', 'failure_type':type(error).__name__,
                   'files_modified':False, 'STOP_REQUIRED':True}
    print(json.dumps(receipt, sort_keys=True, separators=(',',':')))
    raise SystemExit(0 if receipt['RESULT']=='READ_ONLY_ASSESSMENT' else 1)
PY
PE73_HA_ASSESS_EXIT_STATUS=$?
printf 'PE73_HA_ASSESS_EXIT_STATUS=%s\n' "$PE73_HA_ASSESS_EXIT_STATUS"
~~~

Actual observations still required for existing contract acceptance: HA version and
actor/service-response capability, actual config/runtime access and secure ancestor/
ACL/owner/mode/atomic-filesystem support; existing integration/resource inventories;
actual Dashboard/view/layout/export and live storage-resource/admin capability;
observed /local mapping and already-loaded-resource state without lazy migration;
current disabled roles and controlled delivery responsibility; actual private trust
paths/security/certificate/key consistency, issuer/key/SPKI, addresses and independent
operator/Asset ACL. The command intentionally leaves live authentication and private
trust validation UNKNOWN. It does not request secrets in chat or claim observation
of facts it cannot read. Native endpoint binding must be completed using these
actual supported interfaces inside PE-7.3, not another architecture/research phase.

Exactly one next action: operator-run this consolidated read-only PI5 capability/
integration assessment and return its sanitized receipt, to bind the existing
native candidate to actual facts before any installation authority. No deployment,
PI3/PI5 access by Codex, staging, commit, push, activation or PE-7.4 work here.

### PE-7.3 HA OS delivery compatibility correction and runtime protection

Classification: CURRENT PREPARATION — Windows correction validated; native delivery
not established. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. No staging/publication,
production access, deployment or activation in this correction.

Authority: owner-supplied “HA OS Delivery Compatibility Correction and Long-Term
Runtime Protection”, 2026-10-27. The previous69-test preparation remains above as
history. Its PI3 NativeFS reuse and path-prompt assessment are superseded by this
bounded implementation, without altering the accepted HA architecture.

**Established production facts (OPERATOR_SUPPLIED, not newly observed by Codex):**
PI5 HA192.168.100.251, HA OS/Raspberry Pi5 aarch64, Core2026.10.4; Terminal0:0;
/usr/bin/python3, /usr/bin/ha and /usr/local/bin/docker available; /config and
/homeassistant expose custom_components/www; four delivery files absent; Core
container visible. Core UID/GID, shared mount/object identity and destination safety
remain unverified. Completed PI3 evidence and its limitations remain unchanged.

**Confirmed defect and correction:** HA factory inherited PI3-specific1000:1000
file ownership. It now creates a closed-scope one-shot HA publisher, not a generic
root interface. The public four-file payload remains pinned to immutable PE-7.1
51398bab4e2293b578b2cdac2d0740c3738cab2f; Dashboard/package are private references,
never replacements for active YAML. No original runtime or contract bytes change.
The production factory accepts no arbitrary root, owner or saved admission flag.

Publisher credentials must be actual UID/EUID/GID/EGID0. Public code/frontend files
0644 are owned by the proven Core process UID/GID, which may itself be0 only when
independently established. Private transaction directory0700 and records0600 are
0:0, excluding unauthorized unprivileged readers; they do not isolate against other
privileged root processes. Creation-time fchown/fchmod apply only to newly created
exclusive descriptors in the closed target set. No recursive operations, existing
directory ownership/mode corrections, arbitrary paths or secret provisioning.

**Identity/security admission:** exact local Docker bind mappings, no nested config
mounts or user remapping; unique numeric Core Python PID/UID/GID, same user namespace,
stable process birth/boot/container/image, and actual Core /proc/PID/root/config
descriptor identities must match Terminal ancestors and required directories.
Matching Source strings alone cannot admit delivery. Existing host-PID visibility
and permitted proc reads are necessary. If unavailable, return the precise blocker;
no docker exec, setns, new privilege, new dependency or container reconfiguration.
Required existing root/custom_components/hioc_operator/www/backups directories must
be secure and Core-traversable. Missing directories stop before any mkdir/write;
this task does not invent directory provisioning authority. Unsupported ACLs,
unreadable ACL state, symlinks, hard links, unsafe parents, owner/mode mismatch,
identity replacement and pre/post-operation security drift refuse admission.

**Transactions/recovery:** private before/stage/reference/disabled-trust files,
durable pending journal, exclusive creation, fsync, atomic replace (NOREPLACE for
absent destinations), installed readback and fresh context checks remain. No
mutation retry, automatic rollback or release after uncertainty. Fresh sessions
may inspect a safe existing transaction read-only but cannot reuse it for another
deployment. Separate explicit recovery may restore only a fully verified terminal
DELIVERED_DISABLED journal after supported-API Dashboard/resource restoration and
fresh guard checks. Pending/incomplete transactions require explicit disposition;
no blind adoption. Backup bytes and exact installed identities are rechecked.
One defined whole-process authorization; no operation prompts or invented blanket
authority for unexpected recovery. The standing executive decision remains verbatim
in the unchanged successor authorization record.

**HA/trust boundaries:** existing authenticated WebSocket, supported resource/card
registration, private full exports, additive layout and unrelated-resource protection
are preserved. No direct .storage edits or Dashboard mode migration. Trust packet
remains disabled/offline and is not installed TLS material, provisioned keys or live
ACL authorization. Actual authenticated connection, live disabled guard and two-host
trust validation are still explicit unqualified native input ports. Static installed
HA source capability observations are not proof of authenticated live APIs.

**Long-term non-regression:** accepted runtime artifacts remain byte-identical and
introduce no publisher or transaction-file dependency. Normal device/IP/entity/room
changes, observation reconciliation and incidents do not invoke deployment. Assets,
operator notes/policies, identities, history and unrelated configuration are outside
the publisher write allowlist. Code updates do not imply migrations, policy resets,
trust rotation or activation. New authorized software payloads require future exact
artifact/transaction governance, not a permanent Core version pin. Boot/image binding
is specific to one transaction. PI5 delivery failure has no PI3 filesystem/network,
MQTT, incident/offline fabrication or service-control operation. Deferred roadmap
capabilities are not implemented here.

**Focused validation:** one consolidated native-Windows unittest harness selects
test_pe73_ha_delivery, test_pe7_ha, test_pe7_security and test_pe7_dashboard with
sys.path[:0]=['tests','pi4/lib'], shell-free PATH and HIOC_TEST_SHELL cleared.
Final result111 run111 passed,0 failures,0 errors,0 skipped; exact three executable/
test hashes unchanged across the run. Covers root/Core identity separation, private
access, descriptor/path/ACL/link/ownership drift, missing prerequisites, payload pins,
backups, atomic/readback failures, interruptions, fresh-session explicit recovery,
resource conflicts, disabled behavior, persistent-state and runtime independence.
Windows fixtures explicitly model POSIX credentials/dir_fd behavior; no claim of
native Linux chmod/chown/fsync/rename or production qualification. Earlier42-run
fixture attempt had41 passes/1 error from a Windows inode-change-time model mismatch;
the fixture was corrected without weakening production checks. Interim107/107 and
109/109 passes are retained as test history; final111/111 supersedes them.

- `tools/pe73_ha_delivery.py`: SHA-256 `5e2238afeb584b279fe9b0e2de9ff4b5fa3cc5724a3be028be25131c64b34e1f`.
- `tools/pe73_ha_assess.py`: SHA-256 `7437c9d585ae288094a39b30f55adfb4aad66c8502744fa121ae03dbbdc1f350`.
- `tests/test_pe73_ha_delivery.py`: SHA-256 `0eebe7e1c6706b13b19c1f6078b989d2a51533b17965d3e617d24e664ea73693`.

**Preservation:**13 immutable PI3 and six immutable HA source pins verify;39 successor
identities (only two current-document identity entries refreshed) and449 protected
identities verify. Accepted contract, approved amendment, controller, maintenance
provider, original executive instruction and completed PI3 evidence are unchanged.
Exactly the original six candidate paths; three tracked modifications, three new
untracked paths, empty index, unchanged stash/main/origin and no unexpected paths.

#### Consolidated read-only PI5 qualification

Ready only for the existing operator-controlled PI5 Terminal environment using
already observed Python/Docker paths and0:0 identity. No paths to discover, prompts,
unpublished repository files, HA import, reload/restart, container exec, secrets or
credential contents. Reads local Docker metadata, kernel identities, directory/
.storage metadata only, and bounded public installed HA source through stdout tar
without extracting files. Never invokes /usr/bin/ha or HA live APIs. No container,
ownership, permission, service or runtime changes. Native mutation qualification,
live authenticated HA/Dashboard exports/selection/disabled guard and actual trust
identities remain explicitly NOT_OBSERVED; no secret values requested in chat.

PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION with exit0 proves only that bounded
read-only binding. BLOCKED_READ_ONLY_QUALIFICATION with exit1 reports missing proof,
including host-PID visibility, unsafe/missing directories or nonidentical objects.
Neither receipt is native deployment authorization/readiness. No automatic retry or
workaround. Preserve JSON and immediate shell exit-status line as OPERATOR_SUPPLIED.

~~~sh
/usr/bin/python3 -I -S -B - <<'PY'
import ast

import hashlib

import json

import os

from pathlib import Path

import stat

import sys

import errno

import re

import socket

import subprocess

import ctypes

import io

import tarfile

def metadata(path):
    """No following symlinks, no implicit ownership correction."""
    for parent in (path, *path.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('SYMLINK_PATH')
    info = path.lstat()
    return {'device':info.st_dev, 'inode':info.st_ino, 'uid':info.st_uid, 'gid':info.st_gid,
            'mode':format(stat.S_IMODE(info.st_mode), '04o'), 'links':info.st_nlink,
            'type':'DIRECTORY' if stat.S_ISDIR(info.st_mode) else 'REGULAR' if stat.S_ISREG(info.st_mode) else 'OTHER',
            'mtime_ns':info.st_mtime_ns, 'ctime_ns':info.st_ctime_ns}

class QualificationError(ValueError):
    pass

def require(value, code):
    if not value:
        raise QualificationError(code)

def anchor(info):
    return {'device':info.st_dev, 'inode':info.st_ino, 'uid':info.st_uid,
            'gid':info.st_gid, 'mode':stat.S_IMODE(info.st_mode)}

def directory_chain(root, core_uid, core_gid):
    """Read-only descriptor proof; no pathname fallback or mutation experiment."""
    result = {}
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    held = [fd]
    links = []
    try:
        parts = [('/', None)] + [(part, part) for part in Path(root).parts[1:]]
        absolute = ''
        for label, part in parts:
            if part is not None:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
                links.append((fd, part, child));held.append(child);fd=child
                absolute += '/' + part
            info = os.fstat(fd)
            require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,core_uid)
                    and not stat.S_IMODE(info.st_mode) & 0o7022, 'UNSAFE_DIRECTORY')
            # Do not assume that root or capabilities bypass an unreadable parent.
            shift = 6 if info.st_uid == core_uid else 3 if info.st_gid == core_gid else 0
            require((stat.S_IMODE(info.st_mode) >> shift) & 1, 'CORE_TRAVERSAL_NOT_ESTABLISHED')
            for name in ('system.posix_acl_access','system.posix_acl_default'):
                try:
                    os.getxattr(fd,name)
                except OSError as error:
                    require(error.errno == errno.ENODATA, 'ACL_STATUS_UNKNOWN')
                else:
                    raise QualificationError('ACL_PRESENT')
            result[absolute or '/'] = anchor(info)
        for parent,name,child in links:
            require(anchor(os.stat(name,dir_fd=parent,follow_symlinks=False)) == anchor(os.fstat(child)), 'ANCESTOR_DRIFT')
        return result
    finally:
        for descriptor in reversed(held):
            os.close(descriptor)

def bind_mounts(terminal, core, root_metadata):
    """Exact same bind source and identity mapping, never string-prefix trust."""
    require(terminal['id'] != core['id'], 'DISTINCT_CONTAINERS_REQUIRED')
    for value in (terminal,core):
        require(value['running'] is True and value['userns'] in ('','host'), 'USER_NAMESPACE_UNSUPPORTED')
        require(type(value['mounts']) is list, 'MOUNTS_INVALID')
    mounts = [m for m in core['mounts'] if m.get('Destination') == '/config']
    require(len(mounts) == 1, 'CORE_CONFIG_MOUNT_NOT_UNIQUE')
    selected = mounts[0]
    require(selected.get('Type') == 'bind' and selected.get('RW') is True
            and type(selected.get('Source')) is str and selected['Source'].startswith('/')
            and '..' not in Path(selected['Source']).parts, 'CORE_CONFIG_BIND_REQUIRED')
    require(not any(m.get('Destination','').startswith('/config/') for m in core['mounts']), 'NESTED_CORE_CONFIG_MOUNT')
    roots = []
    for mount in terminal['mounts']:
        dest = mount.get('Destination')
        if dest in ('/config','/homeassistant') and mount.get('Source') == selected['Source']:
            require(mount.get('Type') == 'bind' and mount.get('RW') is True
                    and 'idmap' not in str(mount.get('Mode','')).lower(), 'TERMINAL_BIND_UNSUPPORTED')
            require(not any(m.get('Destination','').startswith(dest+'/') for m in terminal['mounts']), 'NESTED_TERMINAL_CONFIG_MOUNT')
            roots.append(dest)
    require(bool(roots), 'TERMINAL_CORE_CONFIG_BINDING_UNAVAILABLE')
    identities = [root_metadata(root) for root in roots]
    require(all((x['device'],x['inode']) == (identities[0]['device'],identities[0]['inode']) for x in identities), 'CONFIG_ALIAS_IDENTITY_CONFLICT')
    # Prefer the explicit HA configuration mount; never accept an arbitrary root.
    return '/homeassistant' if '/homeassistant' in roots else '/config'

def core_identity(top):
    """Only PID/UID/GID/comm, no command arguments, environment or credentials."""
    rows = top.strip().splitlines()
    require(bool(rows) and rows[0].split() == ['PID','UID','GID','COMMAND'], 'CORE_PROCESS_FORMAT_UNKNOWN')
    found=[]
    for row in rows[1:]:
        cols=row.split()
        require(len(cols)==4, 'CORE_PROCESS_FORMAT_UNKNOWN')
        if re.fullmatch(r'python(?:3(?:\.\d+)?)?',cols[3]):
            require(all(x.isdecimal() for x in cols[:3]), 'CORE_IDENTITY_NOT_NUMERIC')
            found.append([int(x) for x in cols[:3]])
    require(len(found)==1, 'CORE_PYTHON_PROCESS_NOT_UNIQUE')
    return {'pid':found[0][0], 'uid':found[0][1], 'gid':found[0][2]}

class NativeProbe:
    """Fixed local Docker reads and kernel metadata. Never exec, HA API or secrets."""
    def docker(self,*args):
        completed=subprocess.run(['/usr/local/bin/docker','--config','/proc/pe73-no-client-config',
            '--host','unix:///var/run/docker.sock',*args],stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=20,
            env={'PATH':'/usr/local/bin:/usr/bin:/bin','LANG':'C','LC_ALL':'C'})
        require(completed.returncode==0 and len(completed.stdout)<=1048576, 'DOCKER_METADATA_UNAVAILABLE')
        return completed.stdout.decode('utf-8')

    def container(self,identity):
        require(re.fullmatch('[0-9a-f]{12,64}',identity), 'CONTAINER_ID_INVALID')
        template='{"id":{{json .Id}},"image":{{json .Image}},"running":{{json .State.Running}},"pid":{{json .State.Pid}},"userns":{{json .HostConfig.UsernsMode}},"pidmode":{{json .HostConfig.PidMode}},"workdir":{{json .Config.WorkingDir}},"mounts":{{json .Mounts}}}'
        value=json.loads(self.docker('container','inspect','--format',template,identity))
        value['mounts']=[m for m in value['mounts'] if any(m.get('Destination')==p or m.get('Destination','').startswith(p+'/') for p in ('/config','/homeassistant'))]
        return value

    def core_filesystem(self,terminal,identity,root,directories):
        """Source strings alone are insufficient. Compare actual Core descriptor nodes.

        Requires existing host-PID visibility; never docker exec, setns, privilege
        escalation or container reconfiguration. Kernel /proc/PID/root is the sole
        intentional proc magic-link traversal; config descendants remain NOFOLLOW.
        """
        require(terminal.get('pidmode')=='host', 'CORE_FILESYSTEM_NOT_OBSERVABLE_WITHOUT_HOST_PID_VISIBILITY')
        pid=identity['pid'];base=Path('/proc')/str(pid)
        def birth():
            raw=(base/'stat').read_text()
            ticks=int(raw.rsplit(')',1)[1].split()[19])
            fields={line.split(':',1)[0]:line.split(':',1)[1].split() for line in (base/'status').read_text().splitlines() if line.startswith(('Uid:','Gid:'))}
            require(list(map(int,fields['Uid']))==[identity['uid']]*4 and list(map(int,fields['Gid']))==[identity['gid']]*4, 'CORE_PROCESS_CREDENTIAL_DRIFT')
            namespace=os.readlink(base/'ns/user')
            require(namespace==os.readlink('/proc/self/ns/user'), 'CORE_USER_NAMESPACE_NOT_IDENTICAL')
            return {'pid':pid,'start_ticks':ticks,'user_namespace':namespace}
        before=birth();held=[]
        try:
            fd=os.open(base/'root',os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC);held.append(fd)
            config=os.open('config',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd);held.append(config)
            anchors={}
            for relative in ('','custom_components','custom_components/hioc_operator','www','backups'):
                current=config
                for part in Path(relative).parts:
                    current=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=current);held.append(current)
                value=anchor(os.fstat(current));expected=directories[str(Path(root)/relative)]
                require(value==expected, 'CORE_VISIBLE_DIRECTORY_IDENTITY_CONFLICT')
                anchors[relative]=value
            require(before==birth(), 'CORE_PROCESS_REPLACED_DURING_QUALIFICATION')
            return {'process_birth':before,'anchors':anchors}
        finally:
            for fd in reversed(held):os.close(fd)

    def public_capabilities(self, core):
        """Public installed source only, memory tar stream, no extract or HA import."""
        base=core['workdir']
        require(type(base) is str and Path(base).is_absolute() and '..' not in Path(base).parts, 'CORE_PUBLIC_SOURCE_UNAVAILABLE')
        result={}
        for relative in ('components/lovelace/websocket.py','components/lovelace/resources.py',
                         'components/lovelace/const.py','components/websocket_api/connection.py',
                         'components/websocket_api/commands.py','components/frontend/__init__.py','core.py'):
            try:
                completed=subprocess.run(['/usr/local/bin/docker','--config','/proc/pe73-no-client-config',
                    '--host','unix:///var/run/docker.sock','container','cp',
                    core['id']+':'+str(Path(base)/'homeassistant'/relative),'-'],
                    stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=20,
                    env={'PATH':'/usr/local/bin:/usr/bin:/bin','LANG':'C','LC_ALL':'C'})
                require(completed.returncode==0 and len(completed.stdout)<=4194304, 'PUBLIC_SOURCE_LIMIT')
                with tarfile.open(fileobj=io.BytesIO(completed.stdout),mode='r:') as archive:
                    members=archive.getmembers();files=[x for x in members if x.isfile()]
                    require(len(files)==1 and files[0].size<=2097152 and
                            Path(files[0].name).name==Path(relative).name and
                            not any(x.issym() or x.islnk() for x in members), 'PUBLIC_SOURCE_ARCHIVE_INVALID')
                    raw=archive.extractfile(files[0]).read(2097153)
                tree=ast.parse(raw);names={n.id for n in ast.walk(tree) if isinstance(n,ast.Name)}
                names.update(n.name for n in ast.walk(tree) if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)))
                literals={n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and type(n.value) is str}
                result[relative]={'sha256':hashlib.sha256(raw).hexdigest(),
                    'symbols':sorted(names.intersection({'SupportsResponse','current_connection','ResourceStorageCollection','websocket_lovelace_save_config'})),
                    'commands':sorted(literals.intersection({'lovelace/config','lovelace/config/save','lovelace/info','lovelace/resources','lovelace/resources/list'})),
                    'source_support_only':True}
            except Exception:
                result[relative]={'state':'PUBLIC_SOURCE_NOT_ESTABLISHED'}
        return result

    def collect(self):
        self.observations={'paths':{},'production_mutation':False}
        require(sys.platform=='linux' and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0, 'QUALIFIED_TERMINAL_ROOT_IDENTITY_REQUIRED')
        require(socket.gethostname().lower().split('.')[0]!='nutandpihole', 'PI3_TARGET_REFUSED')
        require(all(hasattr(os,x) for x in ('O_DIRECTORY','O_NOFOLLOW','O_CLOEXEC','getxattr','fchown','fchmod','fsync'))
                and all(x in os.supports_dir_fd for x in (os.open,os.stat,os.mkdir,os.unlink,os.rename))
                and hasattr(ctypes.CDLL(None),'renameat2'), 'NATIVE_FILESYSTEM_PRIMITIVES_UNAVAILABLE')
        for root in ('/config','/homeassistant'):
            for relative in ('','custom_components','custom_components/hioc_operator','www','backups',
                             'backups/pe73-ha-delivery-v1','.storage/lovelace','.storage/lovelace_resources','.storage/lovelace_dashboards'):
                name=str(Path(root)/relative)
                try:self.observations['paths'][name]=metadata(Path(name))
                except OSError as error:self.observations['paths'][name]={'state':'ABSENT' if error.errno==errno.ENOENT else 'UNAVAILABLE','errno':error.errno}
                except ValueError:self.observations['paths'][name]={'state':'UNSAFE_PATH'}
        for name in ('uid_map','gid_map'):
            rows=[list(map(int,line.split())) for line in Path('/proc/self/'+name).read_text().splitlines()]
            require(rows==[[0,0,4294967295]], 'IDENTITY_USER_NAMESPACE_REQUIRED')
        options=json.loads(self.docker('system','info','--format','{{json .SecurityOptions}}'))
        require(type(options) is list and not any('userns' in x.lower() or 'rootless' in x.lower() for x in options), 'DOCKER_USER_MAPPING_UNSUPPORTED')
        core_ids=self.docker('container','ls','--filter','label=io.hass.type=homeassistant','--format','{{.ID}}').split()
        if not core_ids:
            core_ids=self.docker('container','ls','--filter','name=^/homeassistant$','--format','{{.ID}}').split()
        require(len(core_ids)==1, 'CORE_CONTAINER_NOT_UNIQUE')
        core=self.container(core_ids[0])
        self._observed_core=core
        identity=core_identity(self.docker('container','top',core['id'],'-eo','pid,uid,gid,comm'))
        self.observations['core']={'container_id':core['id'],'image':core['image'],'process':identity}
        ids=set(re.findall(r'(?:docker[-/]|containers/)([0-9a-f]{64})(?:[/.]|$)',Path('/proc/self/cgroup').read_text()))
        for line in Path('/proc/self/mountinfo').read_text().splitlines():
            cols=line.split()
            if len(cols)>5 and cols[4] in ('/etc/hostname','/etc/hosts','/etc/resolv.conf'):
                ids.update(re.findall(r'/containers/([0-9a-f]{64})/',cols[3]))
        require(len(ids)==1, 'TERMINAL_CONTAINER_IDENTITY_UNAVAILABLE')
        terminal=self.container(next(iter(ids)))
        def root_meta(root):
            return directory_chain(root,identity['uid'],identity['gid'])[root]
        root=bind_mounts(terminal,core,root_meta)
        self.observations['selected_root']=root
        directories={}
        failures=[]
        for relative in ('','custom_components','custom_components/hioc_operator','www','backups'):
            try:directories.update(directory_chain(str(Path(root)/relative),identity['uid'],identity['gid']))
            except (OSError,QualificationError) as error:failures.append({'relative':relative,'code':str(error) if type(error) is QualificationError else 'DIRECTORY_NOT_ESTABLISHED'})
        self.observations['directory_failures']=failures
        require(not failures, 'DESTINATION_SECURITY_OR_PREREQUISITE_NOT_ESTABLISHED')
        visible=self.core_filesystem(terminal,identity,root,directories)
        # Same boot/container/image/process/mount and root anchors must survive every mutation.
        require(self.container(terminal['id'])==terminal and self.container(core['id'])==core, 'CONTAINER_CONTEXT_DRIFT')
        return {'schema_version':'1.0','root':root,'publisher_uid':0,'publisher_gid':0,
            'core':identity,'terminal':terminal,'core_container':core,
            'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'directories':directories,'core_filesystem':visible}

def preflight(probe=None):
    """Machine evidence only, never permission or an install flag."""
    probe=NativeProbe() if probe is None else probe
    try:
        value=probe.collect()
        result={'RESULT':'PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION','filesystem_binding':value,
            'native_delivery_ready':False,
            'remaining':['LIVE_HA_CONNECTION_AND_DISABLED_GUARD','DASHBOARD_VIEW_RESOURCE_EXPORT',
                         'ACTUAL_TRUST_IDENTITIES_AND_PRIVATE_FILE_VALIDATION'],
            'mutation_performed':False,'HA_imported':False,'container_exec_performed':False,
            'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}
    except BaseException as error:
        result={'RESULT':'BLOCKED_READ_ONLY_QUALIFICATION','failure_code':str(error) if type(error) is QualificationError else 'FILESYSTEM_OR_METADATA_NOT_ESTABLISHED',
            'failure_type':type(error).__name__,'mutation_performed':False,'HA_imported':False,
            'native_delivery_ready':False,'STOP_REQUIRED':True}
    if isinstance(probe,NativeProbe):
        result['observations']=getattr(probe,'observations',{})
        if hasattr(probe,'_observed_core'):
            try:result['public_capabilities']=probe.public_capabilities(probe._observed_core)
            except Exception:result['public_capabilities']={'state':'NOT_ESTABLISHED'}
        result['not_observed']=['LIVE_DASHBOARD_EXPORT_AND_RESOURCE_CONFLICTS','LIVE_DISABLED_ROLE_GUARD',
            'PRODUCTION_TRUST_MATERIAL_AND_ACL','FILESYSTEM_MUTATION_BEHAVIOR']
    return result

if __name__ == '__main__':
    result=preflight()
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    raise SystemExit(0 if result['RESULT'].startswith('PASS_') else 1)
PY
PE73_HA_OS_PREFLIGHT_EXIT_STATUS=$?
printf 'PE73_HA_OS_PREFLIGHT_EXIT_STATUS=%s\n' "$PE73_HA_OS_PREFLIGHT_EXIT_STATUS"
~~~

Exactly one next operational action: the operator executes this read-only PI5
qualification once and supplies its sanitized receipt and exit status. No PI3 work,
production installation, stage/commit/push or PE-7.4 action is authorized here.

### PE-7.3 preflight prerequisite review and bounded correction

Classification: CURRENT PREPARATION. Existing six-file candidate only. PE-7.3
IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. No production access, execution, Git staging,
commit or push. The accepted111/111 result and protected historical identities are
retained; this follow-up does not restart implementation or reopen PI3 deployment.

**Actual findings, resolved together:**

1. Fresh installation circularity: the native factory and before-state reader
required custom_components/hioc_operator before the delivery sequence could run.
Neither absent delivery files nor the accepted contract established that directory.
The accepted contract section13 requires guarded artifact delivery with exact paths,
owners, ancestors and backup/rollback; it does not forbid bounded directory creation.
The reader now verifies absence through the secure existing parent, reports an empty
HIOC directory and absent file snapshots without writes. Installation may create
only that exact directory, root-owned0755, after durable pending intent in the private
transaction. Exact descriptor/path identity, ACL, mode, fsync and fresh Core-visible
readback are mandatory. A concurrent directory, symlink, owner/ACL/path substitution
or mismatched process proof refuses continuation. Existing directories are unchanged.

2. The same circularity affected backups when absent. Its creation is now preceded
by an exclusive0600 root-owned `.pe73-ha-directory-intent.json` in the verified Core
configuration root, binding the exact backups path, plan, process reference and
context digest. Only missing backups0700 may follow. The bootstrap is fsynced and
read back before mkdir; created directory identity is retained in the transaction.
Existing bootstrap/transaction state is never overwritten or automatically adopted.
Interruption before/after creation requires disposition; no automatic retry/cleanup.
Backup evidence persists. No recursive mkdir or operator manual workaround.

3. Private backup traversal was unnecessarily required of Core. Publisher-only0700
backup storage does not serve HA runtime. All ancestor security checks remain, but
Core access is required only for public destination ancestry, not private backups.
Publisher and Core identities remain separate; installed files0644 use proven Core
ownership, private records0600 use publisher0:0. No privilege expansion or new trust.

4. Host PID mode was an over-specific implementation predicate, not an observed
HA OS capability or contract requirement. It is no longer demanded. The existing
read-only proc route now requires exact Core container cgroup identity (64-hex ID),
numeric PID credentials, same user namespace and stable process start ticks, followed
by actual Core /proc/PID/root/config descriptor identity comparison. PID-number
collision, hidden cgroup, inaccessible proc, wrong credentials or object mismatch
blocks. No docker exec, setns, privilege/container change or metadata-only fallback.
Whether this existing PI5 Terminal can observe that proof remains genuinely UNKNOWN.

Docker MountPoint metadata reports source/destination/options, not target device/inode.
Docker archive PathStat reports name,size,mode,mtime,linkTarget, not device/inode.
Therefore their equality alone cannot reproduce the accepted descriptor-level proof.
Reference: https://github.com/moby/moby/blob/v28.5.1/api/types/container/container.go
(PathStat and MountPoint). This is an explicit limitation, not proof that PI5 lacks
the necessary existing visibility. No new configuration or production probe is asked
for in this task.

**Remaining preflight requirements inspected:** Python/root identity and Docker
availability are accepted OPERATOR_SUPPLIED facts. Their presence does not establish
the exact local Docker socket, user mappings, Core process/proc observability, mount
identity, destination ACL/ownership or native atomic filesystem behavior. Those are
genuine qualification gates, not contradictions with supplied facts. Existing
custom_components/www are supplied; config aliases are selected by exact binding,
not guessed equivalence. Unknown or multiple Core Python processes stop. Optional
public source capability failure remains non-admitting information, not an exact HA
version pin. There is no further prerequisite provably incompatible with the supplied
facts, and no other missing installation-owned directory in the closed write scope.

**Recovery:** separate explicit recovery after supported-API restoration removes
only an empty HIOC directory whose full recorded identity matches this transaction's
creation. Existing directories are never removed. Identity drift, foreign content,
pending creation/publication or uncertain removal stops and preserves evidence.
Private backup/bootstrap/transaction evidence is deliberately retained, not deleted.
Fresh-session checks remain; neither success nor failure triggers automatic rollback.

**Consolidated validation:** native Windows harness with shell-free PATH,
HIOC_TEST_SHELL cleared and sys.path[:0]=['tests','pi4/lib']; the same four focused
modules: test_pe73_ha_delivery, test_pe7_ha, test_pe7_security, test_pe7_dashboard.
125 run125 passed;0 failures,0 errors,0 skipped. The previous111 tests remain in
the selection, with the obsolete host-mode negative updated to require inaccessible
proof refusal;14 regressions add missing-directory/bootstrap intent, interruption,
substitution, fixed scope, exact/fresh recovery, existing-directory preservation,
observable proc without a host-mode predicate, PID collision, hidden identity,
credential drift and private backup separation. No unrelated historical suite.
Executable/test bytes were unchanged throughout the run. Windows POSIX models
remain synthetic, not production or Linux mutation qualification.

- `tools/pe73_ha_delivery.py`: SHA-256 `4f50112d58a874c88e21b566168b5d78bdb926076008e3a2580ee5029df88c75`.
- `tools/pe73_ha_assess.py`: SHA-256 `83f4effedbe8555e7671e91975f542e10d431b18b0611a9cc6d99d1f3beff418`.
- `tests/test_pe73_ha_delivery.py`: SHA-256 `e44e3efc8957c045a209d45bb8d07da248b724673a5b74bbd9085c477498766c`.

**Preservation:**13 PI3 delivery,39 successor,449 protected and six immutable HA
source identities verify. Only the two current-document identity entries refresh.
493 other tracked files, accepted contract/amendment, controller/provider, executive
instruction, completed PI3 evidence and original111-test report remain unchanged.
Trust architecture, disabled-by-default behavior, supported HA Dashboard mechanisms,
runtime independence and persistent-state isolation remain. No migration/activation,
secret operation or ordinary-device-change deployment dependency was introduced.

The previous embedded operator command is retained as historical preparation,
superseded by the corrected source; it must not be reused as the current preflight.
No new PI5 command is requested or returned in this review. Actual live HA/API,
approved Dashboard selection/export, disabled guard, trust identities and native
filesystem capabilities remain qualification inputs, not accepted observations.

Exactly one next action: bounded independent acceptance of the corrected six-file
candidate before publication or native qualification. No production mutation.

### PE-7.3 HA delivery candidate independent acceptance and controlled publication

Classification: REPOSITORY ACCEPTANCE PASS; production qualification pending.
Authority: owner's Final Independent Acceptance and Conditional Publication request.
Baseline main/origin/main2784ef31da5e4ebc0e75af19695c8cc68c3d04a1. Exactly the existing
six-file HA candidate; no implementation source or test bytes changed during review.

The actual Delivery, scoped native filesystem, NativeProbe and regression logic were
inspected against the15 mandatory acceptance requirements. The accepted PE-7 contract
remains authoritative and byte-identical. Master Plan changes record current evidence
and sequencing only; accepted requirements and historical narratives remain preserved.

1. No inherited1000:1000 HA ownership policy. Publisher credentials, actual Core
process identity, public files0644 and private records0600/directory0700 are distinct.
2. Actual Core-visible descriptor identity must match before mutation. No admission
from saved JSON, root privilege, mount strings, PID mode or branch names alone.
3. Missing integration/backup directories have fixed-path, durable-intent procedures;
private bootstrap precedes missing backup-parent creation. No manual workaround.
4. Host PID mode is not universal. Exact container/process/namespace/birth and
filesystem proof is required; hidden or unavailable evidence refuses continuation.
5. Anchored no-follow traversal, device/inode, owner/mode, ACL, single-link file and
pre/post-operation path checks remain. New descriptors alone receive bounded modes.
6. Four exact immutable HA payloads and necessary private records are the only write
scope. Backup/export, pending intent, exclusive creation, atomic publication and
independent readback remain; failure never retries, rolls back or releases consumers.
7. Explicit recovery uses exact retained evidence and only removes its empty created
directory; unrelated/existing directories and uncertain transactions are not adopted.
8. Runtime independence, persistent Asset/config/history isolation and capability-based
compatibility remain. No permanent HA version pin, migration or discovery coupling.
9. Supported authenticated HA Dashboard/resource calls preserve unrelated content and
export originals. No direct .storage editing, broad YAML replacement or reload.
10. Accepted mTLS, signed actors and independent ACL design is preserved. No production
secrets/identities are invented, installed, exposed or activated. Disabled integration,
editing, evaluator, migration and recurring-function boundaries remain mandatory.
11. Completed PI3 evidence, contracts, amendment, executive decision and protected
artifacts remain unchanged. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.

Validation retained:125 tests passed,0 failures/errors/skips; exact code/test hashes
match source_before/source_after in the retained Windows result. No historical suites
were repeated. All25 static preservation checks independently rerun PASS.13 PI3
delivery identities,39 successor identities,449 protected identities and six immutable
HA source pins verify. Only two current-document successor identity entries refresh.
Diff checks cover tracked changes and all three new files. Actual remote refs/heads/main
was checked against the baseline before publication. Stage/commit scope remains six.

Accepted code/test SHA-256:
- `tools/pe73_ha_delivery.py`: `4f50112d58a874c88e21b566168b5d78bdb926076008e3a2580ee5029df88c75`.
- `tools/pe73_ha_assess.py`: `83f4effedbe8555e7671e91975f542e10d431b18b0611a9cc6d99d1f3beff418`.
- `tests/test_pe73_ha_delivery.py`: `e44e3efc8957c045a209d45bb8d07da248b724673a5b74bbd9085c477498766c`.

Remaining PI5 production requirements, explicitly not established by this review:
- Actual local Docker/proc access, Core identity/user mappings, exact configuration
  mount/object equivalence, secure ancestry/ACLs and ownership.
- Native filesystem mutation/durability/atomic-publication qualification.
- Authenticated live HA capability/disabled guard, /local mapping, supported storage
  resources and approved Dashboard/view export and conflict-free additive delivery.
- Actual production trust identities, private-file/certificate/key consistency and
  independent ACL qualification through existing secure bindings; no secret disclosure.
These are dependent native gates, not repository acceptance failures or authority to
install, provision credentials, change containers, restart or activate functionality.

One next operational action: operator-run the consolidated read-only PI5 qualification
from the accepted preflight. No PI3 or PI5 access by Codex. No deployment, activation,
production mutation or PE-7.4 work in this acceptance/publication operation.

### PE-7.3 Core PID-namespace qualification correction

Classification: CURRENT PREPARATION; focused independent repository acceptance PASS.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. This is the existing checkpoint's narrow
compatibility correction and authorized Git publication, not production execution.
Baseline published commit2d2ecf5b95531b2c514cc4a889aa358f9fc27365.

**New OPERATOR_SUPPLIED evidence:** published qualifier source verification passed;
result CORE_PROCESS_FILESYSTEM_IDENTITY_NOT_OBSERVABLE. Selected root/homeassistant;
Docker-reported Core UID/GID0:0, host PID731186; directory failures none; HIOC integration
absent as expected; production mutation false. Subsequent reads of/proc/731186/stat,
/proc/731186/status,/proc/731186/cgroup,/proc/731186/ns/user,/proc/731186/root each
returned ENOENT(errno2). Terminal PID namespace pid:[4026533213], user namespace
user:[4026531837]. Codex did not collect or repeat these observations. They establish
that the Docker host PID is unavailable in Terminal/proc; no directory-security
failure, permission relaxation or production health assertion follows.

**Confirmed defect:** published NativeProbe.process_birth/core_filesystem interpreted
a Docker host PID as a Terminal-visible PID. Removing a host-mode predicate did not
remove the namespace assumption. That direct Terminal/proc host-PID route is replaced.

**Bounded supported correction:** Docker container exec targets the exact64-hex Core
container ID selected by read-only inspection. The only program is python3 -I -S -B
-c with a fixed embedded metadata script. No shell, TTY, stdin, arbitrary script/path,
--privileged, privilege change, service, mount/config change or retry. It runs under
the already observed numeric Core UID/GID, never guessed from Terminal root. Docker
exec is explicitly disclosed in the receipt; the prior no-container-exec preparation
claim is historical and superseded only for this fixed metadata preflight.

The fixed helper reads only/proc process identity and approved/config directory
metadata. It excludes its own Python PID, requires exactly one remaining Core Python
process, checks actual helper/Core credentials and identity UID/GID mappings, and
pins Core namespace-local PID/start ticks/user namespace before and after capture.
It opens the actual local Core process root through the intentional kernel proc
link and then/config and fixed descendants with descriptor-relative NOFOLLOW.
Each directory's device,inode,UID,GID,mode,ACL absence/traversal and named/descriptor
identity are checked. Missing integration/backups is represented as observed absence,
not a manual prerequisite. Terminal compares every anchor/absence to its secure
configuration-root evidence. User namespace must agree. Docker's host Python PID,
UID/GID and container ID/image/start timestamp/mount metadata are checked again.
Host and namespace-local PID are separate receipt fields; no numeric coincidence,
matching path or mount-source string can establish filesystem equivalence.

No file contents, configuration, environment values, private keys/certificates,
tokens, credentials or HA modules are read by the Core helper. No HA import,
reload/restart, classification, HIOC engine, scheduler, migration, activation or
filesystem write. A transient metadata process is created through supported Docker
exec; it is not a persistent service or HA runtime activation. Inaccessible proc,
unsupported interpreter/exec, ambiguity, ACLs, namespace/credentials/object drift,
helper failure or incomplete output blocks qualification without a workaround.

**Directly related assumptions corrected together:** Core2026.10.4 Dockerfile uses
io.hass.type=core (exact-name fallback retained), not the oldhomeassistant label.
Its working directory/config is not the Python source directory. Optional bounded
public-source reads now use/usr/src/homeassistant/homeassistant, the source-supported
layout. Source inspection remains optional/capability evidence, not admission or a
permanent HA version pin. Unknown layouts remain NOT_ESTABLISHED.
Primary support: https://docs.docker.com/reference/cli/docker/container/exec/ and
https://github.com/home-assistant/core/blob/2026.10.4/Dockerfile . These explain the
API and reviewed source layout; they are not invented observations of PI5.

**Focused validation and independent acceptance:** same four native Windows focused
modules, documented shell-free PATH, HIOC_TEST_SHELL cleared, sys.path[:0]=['tests',
'pi4/lib']. 133 run,133 passed,0 failures,0 errors,0 skipped; exact final
source/test identities unchanged during validation. Simulated isolated Terminal
namespace gives ENOENT for all host-PID paths while fixed Core-local metadata passes;
positive descriptor capture is modeled with actual temporary Windows files plus
explicit POSIX namespace/ownership seams. Negative cases include device/inode/mode/
owner mismatch, unexpected directory, process/credential/user-namespace drift,
blocked/incomplete helper output, ACL presence and process restart. Fixed-script AST
and exact argv checks prohibit write/shell/network/HA operations. Native Linux/PI5
qualification is not inferred from synthetic tests.

An initial85-test attempt had84 passes/1 fixture error: Windows fixture translated
Core/config on open but not its final named stat. The fixture alias was corrected;
production identity checks were unchanged. Failure evidence is retained externally.
Final passing run supersedes that fixture attempt. No unrelated historical suite.

Focused independent inspection confirms the new helper is fixed/read-only, current
container/identity/object evidence is mandatory and uncertain outcomes fail closed.
The change is within the owner's authorization prohibiting unrestricted execution;
it does not relax the accepted security contract. No mandatory repository acceptance
blocker remains. No separate consequential-step approval prompt is introduced.

- `tools/pe73_ha_delivery.py`: SHA-256 `4f50112d58a874c88e21b566168b5d78bdb926076008e3a2580ee5029df88c75`.
- `tools/pe73_ha_assess.py`: SHA-256 `da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443`.
- `tests/test_pe73_ha_delivery.py`: SHA-256 `3a2da88bf8235f6157ca23e1f1590d21544b7b954253267e54aaf592e85eca9f`.

**Preservation:** publisher/transaction implementation is byte-identical to the
accepted release. Four HA payloads and two HA references,13 PI3 delivery,39 successor
and449 protected identities verify. Only the two current-document successor entries
refresh. Historical contracts, maintenance amendment, executive instruction, completed
PI3 deployment, original125-test acceptance, disabled roles, trust architecture,
backups/recovery, runtime independence and persistent Asset/state isolation remain.
Exactly five existing paths change: assessment, its existing delivery tests, Master
Plan, implementation evidence and candidate record. No other paths or new files.

Remaining native requirements: successful exact Core-local metadata capture through
existing Docker/installed Python; exact directory/security equivalence; native atomic
publication/durability; authenticated HA capabilities/disabled guard, approved live
Dashboard/view/resource export; actual trust/private-file/independent ACL bindings.
No secret values are requested in chat. Unknown capabilities block dependent action.

One next operational action: operator-run the single read-only PI5 qualification
command bound to the newly published immutable assessment commit and SHA-256, retain
its sanitized receipt and immediate exit status, and stop. No installation follows.

### PE-7.3 live API, Dashboard and disabled-role qualification

Classification: CURRENT PREPARATION; LIVE_QUALIFIER_IMPLEMENTATION=PASS;
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_BOUNDED_READ_ONLY_REPOSITORY_PUBLICATION.
PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. This implements the existing delivery
qualification only. No new checkpoint, architecture, production access or closure.
Baseline main/origin da630dd9cac20b784a6b433de614bfe323d4576f.

**Accepted OPERATOR_SUPPLIED filesystem qualification (not repeated):** source
da630dd9cac20b784a6b433de614bfe323d4576f; result
PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION; exit0. PI5 HA192.168.100.251,
HAOS/Core2026.10.4, Terminal/Core UID/GID0:0. Terminal/homeassistant and Core/config
refer to the same actual objects. Device/inode, ownership, mode, namespace, process
and existing required directories passed. Missing hioc_operator installation directory
is expected/supported. No production mutation. Installed public source established
Lovelace configuration/resource storage, WS context and service-response support.
These are operator observations, not Codex-collected facts or new production claims.

**Actual existing interfaces:** pe73_ha_delivery.READs/observe require admin,
get_config/get_services, storage resources/config; fresh host/disabled/exclusive/
resources_loaded/local_mapping/storage_dashboard/capability_identity guards; exact
four-artifact publication and six immutable source references. Existing add_card
supports unique masonry/cards or sections views; panel/unknown/duplicate/editor
conflicts stop. The new qualifier adds only the supported get_panels and
lovelace/dashboards/list read commands for actual target discovery, never an alternate
editing/write interface. Existing delivery/assessment source is unchanged.

**Supported authentication, with explicit limits:** official Home Assistant app
communication documentation specifies ws://supervisor/core/websocket and the app's
already-present SUPERVISOR_TOKEN in the normal auth handshake, conditional on the
app's existing homeassistant_api permission. No token is copied from files/proc/
Docker, requested from the operator, printed, placed in arguments, sent to HIOC or
GitHub, persisted or created. The token is used only in RAM for that internal protocol.
No permission elevation or add-on reconfiguration. The fixed peer is Supervisor
172.30.32.2:80; no redirects, alternate hosts, retry or credential fallback. Native
token/permission availability remains unobserved until the single operator action.
Root is never used as proof of API authority. A successful protocol still requires
actual auth/current_user admin and a nonempty hashed principal; no raw identity,
credential metadata or private exceptions in the receipt. Server WS user checks
establish active connection admission; proxy admin does not establish a non-system
human editing actor. PE-7 authenticated interactive actor/allowlist/assertion/ACL
requirements remain separate and unchanged.

If existing app authentication is absent/denied, the tool stops without scanning or
requesting secrets. Smallest supported fallback: open the existing HA frontend in
the ordinary browser, log in as an existing administrator using the normal HA login
and keep that authenticated same-origin session. Its supported hass.callWS interface
can carry the same read-only allowlist; no access-token export, new credential or
permission broadening. No browser session or fallback execution is invented here.

**Read-only/resource safety:** a fixed allowlist contains only eight supported reads;
no service call, dashboard/resource write, reload or mode switch is possible through
the transport. Frame/JSON/message/deadline/request/catalog/view/resource budgets,
response IDs, duplicate-key checks and sanitized failures are enforced. Socket closes
on completion/failure; uncertain close cannot report PASS. No HIOC/HA import, file
operation, lock, subprocess, filesystem inspection or installation is performed.
Normal API connection/cache handling is not evidence of universal runtime immutability.

Core2026.10.4 resources/list can lazy-import a legacy default resources key and save
configuration. The qualifier therefore first observes the exact default storage
config and refuses any legacy key. A named lovelace shadows config(None), so that
case cannot prove the true default import source and blocks before listing resources.
Unknown/default YAML source or unsupported APIs also block. No .storage or unsafe
shortcut is used. Catalog/config reads preserve YAML dashboards without loading or
migrating them. The guard evaluates observed source state; it is not an exclusive
transaction or proof of no concurrent external configuration changes. The native
delivery's separate fresh exclusive guard remains mandatory.

**Dashboard/resource output and backup:** retain existing HIOC layout. Repository
hioc_dashboard_v2.yaml is a reference with executive/operations/diagnostics/inventory/
network/server views, not permission to overwrite the live dashboard. All compatible
observed storage dashboard/view choices are returned, preferring existing HIOC labels
for operator consideration; no target is selected even if unique. YAML and unsupported
layouts remain untouched. Only bounded selection labels, layout/suitability, digests
and editor-conflict flags are emitted. Card/entity content, resource URLs/query
parameters and raw API errors are not emitted. Normalized/encoded editor paths are
conflicts. Full observed config/resources are used in memory; later existing
Delivery.prepare must export both exact API objects into private transaction backups
before any publication. This qualifier creates no backup and authorizes no write.
Existing accepted www/Core filesystem and installed frontend source support the
/local mapping capability. The actual live route is not established merely by
an absent editor or HTTP404; live_guard.local_mapping stays false pending proof.

**Disabled roles and trust reconciliation:** absent component AND absent services
establish HA integration inactivity without a circular requirement to run it first.
A present role requests actual disabled evidence; it is not called unsafe merely
because present. HA APIs cannot prove current PI3 evaluator, scheduler, migrations,
notifications or manual caller exclusion; disabled/exclusive guards remain false,
explicitly unestablished, and native_delivery_ready is always false. API-discovery
PASS is not an executable native guard or frozen authorization report.
Contract sections5,7,13 require actual trust/private-secret placement and guarded
integration/UI/trust delivery. No authority was found to skip existing strict
trust_preflight for disabled file staging. It remains before transaction creation:
identity,ha_private_files,backend_private_files,certificate_pair,assertion_pair,
spki_pin,independent_acl must all pass. Later production steps require owner-selected
private endpoint/address/port and issuer/key ID; valid mTLS CA/certificate/key pairs;
separate matching assertion key; client SPKI pin; observed0600 files/0700 private
parents; explicit existing human HA operator allowlist and independent exact-Asset/
operation backend ACL. Keep every enable flag false; securely provision under later
production authorization, never send secret values in chat/Git/receipt. No trust
material, ACL grant, configuration or service is created by this task.

**Focused native validation:** documented bundled Windows interpreter, repository
root, shell-free PATH, HIOC_TEST_SHELL cleared, sys.path[:0]=['tests','pi4/lib'].
163 distinct final focused tests supported,163 passed,0 failures,0 errors,
0 skipped,0 class-level skips. Initial consolidated run:161/161. Source review then
added a normal-mode guard because safe mode can return an empty resource list without
loading resources; final new-module run59/59, retaining104 unchanged delivery passes.
Total actual test executions220, distinct final selection163; no failure was hidden.
Selection: test_pe73_ha_live_qualify and existing test_pe73_ha_delivery only. Exact
tool/test and existing publisher/assessment hashes remain unchanged during the run.
Positive/negative tests cover existing admin proxy authentication, missing/denied
auth, protocol/frame/response/size/deadline checks, unsupported reads, storage/YAML,
legacy-import/shadow guards, conflicting resources, view/default-dashboard handling,
absence/disabled role truthfulness, no target selection, redaction, per-read failure
isolation, cleanup failure and zero mutation capability. Existing delivery tests
retain trust, backup, atomic publication, interruption, exact recovery and ownership
protections. No repeated filesystem qualification, production action or unrelated
historical suite. Native PI5 API results remain UNKNOWN until the operator runs it.

**Focused independent acceptance:** actual allowlist, source-supported proxy scope,
read-side import refusal, backup/trust interface mapping, failure/cleanup output and
negative tests inspected independently of the passing summary. No new production
authority or acceptance gate is invented. Mandatory repository acceptance passes;
conditional native capabilities and unresolved guard/trust facts remain explicit.

- `tools/pe73_ha_live_qualify.py`: SHA-256 `cf9e172595c05ca81a0bfec991c33f9ac7be756e30fb25dc8a6ac065d1e9a1cc`.
- `tests/test_pe73_ha_live_qualify.py`: SHA-256 `76b53ac64d7b1148baa8dd4810b9ec16c82b935726ce12e0a8e143e94f4d87f2`.

**Preservation and publication scope:** exactly five files: new qualifier and its new
tests, Master Plan, this append-only evidence and the existing candidate record.
Only two current-document successor identities are refreshed in that record; all39
current successor identities verify, all449 protected identities remain unchanged.
All13 PI3 payload identities and all six immutable HA source identities remain.
496 other tracked files, original contract/amendment, executive instruction, PI3
deployment evidence, accepted delivery and assessment source, runtime independence,
persistent-state isolation, disabled defaults and history remain byte-identical.
Commit/push and clean-tree/remote identity checks are inside this authorized task;
no PI3/PI5, production, credential generation, reload, restart, migration or activation.

**One next operator action:** on PI5 Terminal only, run the single published,
SHA-256-bound in-memory live qualifier; retain its sanitized report and immediate
exit status and stop. It neither repeats accepted filesystem checks nor installs
anything. BLOCKED means the precise missing API/auth/source/selection capability,
not unsafe filesystem operation or permission to bypass the gate.

Primary support reviewed:
- https://contributors.home-assistant.io/apps/guides/communication/
- https://contributors.home-assistant.io/frontend/reference/hass-object/
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/auth/__init__.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/websocket.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/resources.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/dashboard.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/frontend/__init__.py

### PE-7.3 live Dashboard-shape correction

Classification: CURRENT PREPARATION; independent focused acceptance PASS for this
bounded correction/publication. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED. Baseline
5fc1560a4be75e509e351eaf976364ed9bec62f1, main/origin synchronized and clean.

**New OPERATOR_SUPPLIED PI5 receipt:** published source SHA-256 verification PASS;
authenticated Supervisor proxy WebSocket PASS; administrator principal PASS for
read-only discovery; integration absent/inactive; Lovelace resource mode storage.
Dashboard discovery stopped with DASHBOARD_SCHEMA_OR_LIMIT; Dashboard results empty
because discovery stopped. Production mutation false; exit1. The receipt does not
include the returned config's type, presence/type of views, or view count. Those
actual runtime details remain UNKNOWN; no malformed-Dashboard claim, strategy guess
or invented production observation. Accepted filesystem qualification remains PASS,
accepted/not repeated. Codex did not access PI3/PI5 or collect these observations.

**Established software defects and source authority:** Core2026.10.4
websocket_lovelace_config returns config.async_json directly; LovelaceStorage builds
JSON from the raw stored config, not a guaranteed static-view wrapper. Its pinned
frontend manifest selects20260930.5, whose LovelaceRawConfig union is static views OR
strategy. A strategy can legitimately omit views. Thus views(config)'s universal
static-list prerequisite was incomplete.32 was a qualifier-local cap, not an HA
schema maximum, and one exception discarded remaining Dashboard discovery. The
original error combined several predicates, so the specific on-host predicate is
not proven by the supplied receipt. Static support is evidence about software, not
proof of the actual production config. No runtime JSON-string unwrap or speculative
response-wrapper interpretation is introduced.

**Correction:** fixed-schema diagnostics expose only JSON type, top-level key count,
views presence/type/count, strategy presence/type and legacy-resources-key presence.
No arbitrary key names, strategy type values/options, entity IDs, card contents,
private config, resource URLs/query values, principal IDs or credentials are output.
Known label fields remain bounded/control-safe and may be null if unreportable;
canonical config digests remain evidence, not reconstructed historical fingerprints.
Static views up to256 are safely inspected;33 is accepted.256 is an explicit local
budget, not an HA validity rule. Larger configs report the actual count, all omitted
views and LOCAL_VIEW_BUDGET_EXCEEDED; they are not offered as targets. The request,
message/JSON/deadline/catalog/resource bounds remain finite. Catalog overflow or
unknown/duplicate selector rows preserve bounded discovery but keep resources blocked.

Strategy-declared Dashboards and views are observed as generated/not static. The
qualifier never evaluates strategy code, substitutes generated output, takes control,
creates a Dashboard, changes mode or selects a target. Missing/non-list views and
unexpected top-level types are unqualified observations, not assertions of malformed
HA config. A config_not_found read records no static export and continues. Read
authorization/unsupported-command/transport errors still stop; no retry or permission
fallback. Completed choices remain in the report if a later read fails.

**Related assumptions corrected together:** view path/title/cards/sections are
optional in HA's frontend schema. The unchanged existing Delivery.add_card needs an
explicit unique path and supported static cards/sections list for its narrow additive
operation. Such absence is therefore a target limitation, not an HA schema failure;
no synthetic path, empty list or index is invented. Unknown/non-object view rows
cannot qualify that Dashboard because the existing publisher iterates every row.
Other valid Dashboards remain available. Catalog title/control-character problems no
longer discard all discovery; unsafe/ambiguous selectors are never requested. Unicode
alphanumeric selectors retain the same bounded non-traversal character restriction.
Unsupported resource_mode values are redacted rather than echoed. Panel config null/
unexpected shapes get an exact public blocker instead of a raw attribute failure.
Resource-response shape/count diagnostics are similarly sanitized; incomplete
resource conflict evidence remains fatal to qualification.

**Legacy-resource and security gates:** no resource API is called merely to recover
Dashboard discovery. Catalog/default-source proof remains separate from view-shape
analysis. Named lovelace shadowing, incomplete catalog, unreadable default, unknown
default type or ANY legacy resources key blocks resources/list. A successful null
default response is now explicitly distinguished from config_not_found and blocks;
it cannot establish absence. Missing views alone in a dictionary does not imply a
legacy key exists or allow bypass of that check. Dashboard shape problems never
relax authentication, strict read allowlist, framing/context budgets, private-error
sanitization, editor conflicts or native guards. No new service/read API or new auth.
Native delivery remains false; trust and fresh cross-host disabled/exclusion/local
mapping evidence are neither inferred nor waived. Existing transaction and backup
publication, rollback/recovery algorithms and strict trust_preflight are unchanged.

**Validation:** bundled Windows native interpreter, repository-root working directory,
documented shell-free PATH, HIOC_TEST_SHELL cleared, sys.path[:0]=['tests','pi4/lib'].
81 tests run,81 passed,0 failures,0 errors,0 skipped,0 class-level skips. Exact tool/
test hashes unchanged through run. The consolidated focused module covers all59
previous qualifier regressions (three expectations corrected to the new reporting
semantics) plus22 new cases: missing/non-list/unexpected responses, strategies,
33/excessive view counts, mixed YAML/storage, valid Dashboard preservation, optional
fields, incompatible rows, unknown catalog, partial transport failure, default-null
and legacy-resource protection, redaction and panel/resource shape failure. No
unrelated historical suite rerun; previous104 delivery tests retain exact unchanged
source/test evidence from5fc1560. No production command was run by Codex.

**Focused independent acceptance:** inspected the actual source diff and negative
cases independently of summary counts: only successful config_not_found and safe
unsupported shapes continue; security/transport failures stop; the resource gate is
not weakened; publisher-incompatible/generated targets are never eligible; no private
payload is copied into diagnostics. Missing actual runtime shape is intentionally
deferred to this single sanitized operator receipt, not guessed. Repository acceptance
passes for publication; production qualification/installation is not claimed.

- `tools/pe73_ha_live_qualify.py`: SHA-256 `6c4eda9cec7a1b8db0ca82dec8981eb837ea55041381615a01f59d009903db07`.
- `tests/test_pe73_ha_live_qualify.py`: SHA-256 `11214b00aaeb3b7e3fd319fa9b6c587049119b271d3f6730214fa480a17b5100`.

**Preservation:** exactly five existing paths change: qualifier, its tests, Master
Plan, append-only implementation evidence and existing candidate record. Only two
current-document successor identities refresh; all39 current bindings and all449
unchanged protected identities verify.13 immutable PI3 delivery and six immutable HA
source identities verify.496 other tracked files, original PE-7 contract, maintenance
amendment/executive instruction, PI3 deployment, accepted filesystem evidence, old
production failure and prior test evidence remain unchanged. No HA artifact, service,
credential, Dashboard or runtime change. Stash preserved. PE-7.3 remains IN_PROGRESS;
PE-7.4 remains NOT_AUTHORIZED.

One next action: operator-run the single read-only PI5 qualifier from the newly
published immutable commit with SHA-256 verification in memory; capture sanitized
shape/choice/resource report and immediate exit status, then stop. No deployment,
resource write, YAML migration, selection, reload, activation or follow-on action.

Primary source references reviewed:
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/websocket.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/dashboard.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/frontend/manifest.json
- https://github.com/home-assistant/frontend/blob/20260930.5/src/data/lovelace/config/types.ts
- https://github.com/home-assistant/frontend/blob/20260930.5/src/data/lovelace/config/view.ts
- https://github.com/home-assistant/frontend/blob/20260930.5/src/panels/lovelace/strategies/get-strategy.ts

### PE-7.3 exclusive HIOC Dashboard and resource-source qualification

Classification: CURRENT PREPARATION; independent focused acceptance PASS for this
bounded repository correction/publication. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
Baseline c5274abccb1637335fbf9a9095716e40ace986b4; clean synchronized main/origin.

**Accepted OPERATOR_SUPPLIED production evidence:** authenticated read-only HA WS
access passed; resource mode storage; six registered Dashboards observed; existing
HIOC Dashboard v2 confirmed at url_path hioc-dashboard-v2; its six existing views
and paths read successfully; no existing HIOC Asset Editor card detected; no
production mutation. Qualifier stopped DEFAULT_STORAGE_SOURCE_NOT_ESTABLISHED.
No claim of resource-conflict PASS, actual registry contents or production trust
follows from that stop. No raw get_panels result was supplied in this summary; the
specific failing metadata field is not invented. Filesystem PASS remains accepted,
not repeated. Codex did not access PI3/PI5 or execute production qualification.

**Owner-established exclusive interface (current governed requirement):** the existing
HIOC Dashboard v2, hioc-dashboard-v2, is the sole interface for all HIOC functionality,
including manual Asset/device controls. No alternative Dashboard, separate management
UI, Dashboard-selection exercise, duplicate or migration is authorized. This narrows
current delivery to the existing accepted interface; it does not rewrite historical
contracts, change controls/authentication/trust, or authorize feature activation.
Repository homeassistant/dashboards/hioc_dashboard_v2.yaml defines six reference paths:
hioc-v2-executive, hioc-v2-operations, hioc-v2-diagnostics, hioc-v2-inventory,
hioc-v2-network, hioc-v2-servers. Preserve their existing navigation/layout/content.
The supplied production summary establishes six views/paths read; it does not
separately supply their string values or complete configuration bytes. Reference
definitions are repository facts, not invented per-path production observations.
The qualifier freshly reports the actual six observed paths and configuration digest;
it never rewrites them to match YAML, chooses a placement view or offers another UI.
The existing guarded delivery plan is governed to use hioc-dashboard-v2 exclusively;
its general library interface is not authority for another target. No native delivery
CLI or Dashboard change is introduced here. Earlier choice-oriented preparation is
historical and superseded by this explicit owner decision, not deleted or rewritten.

**Confirmed predicate defect and source-supported proof:** HA2026.10.4's
_async_ensure_default_panel registers a compatibility lovelace panel without passing
config. Therefore a required get_panels['lovelace']['config'] dictionary is not a
supported universal precondition and does not establish resource safety. Setup creates
LovelaceStorage(hass,None), shares it with ResourceStorageCollection, and stores it
under dashboards[None]. The config WS handler chooses that object when no named
lovelace shadows it. Catalog listing includes named configs, so a complete bounded
catalog without that alias binds the read to the real import source. Resource loading
imports/saves only if its fallback config contains resources; absent config raises
config_not_found through the same handler. This is object-flow evidence from the
supported implementation, not matching Dashboard names or panel metadata.

**Bounded correction:** remove the irrelevant panel predicate and get_panels request,
not the import safeguard. Read only the uniquely registered storage HIOC target,
plus config(None) solely as the legacy import probe. Its content is not enumerated
as another Dashboard/target. Target must still expose six distinct existing paths,
no editor card and a compatible static-addition capability; no automatic rebuild,
missing-path/card insertion, generated strategy evaluation or fallback target.
Read-only catalog metadata is necessary for unique target/source binding; unrelated
Dashboard configs are never fetched or reported. The WS config selector itself is
restricted to the fixed target or None. No target choice field or selection request.

Require storage resource mode, a complete typed bounded catalog, no named lovelace,
and either an actual default dictionary without ANY resources key or a genuine
config_not_found response. Successful null, unsupported type, inaccessible source,
unknown catalog row, omitted entries, legacy key or named shadow blocks before any
resources/list request. Source shape diagnostics are sanitized and do not disclose
configuration. No .storage read, bypass, alternate API, resource initialization call
merely for discovery, reload or migration. The compatibility panel may be absent,
config-less or null without defeating the separate actual-source proof.

Global resource listing is necessary to check the one proposed local resource.
The bounded receipt exposes count, canonical registry digest and HIOC editor conflict
fingerprints only; no unrelated per-resource data, URL/query, cards/entity IDs or
private values. /local/hioc-asset-editor.js and encoded/same-editor path conflicts
remain fatal. A successful result is bounded read-only resource/UI qualification,
not native delivery readiness or proof of no concurrent external change. The later
fresh exclusive guard, exact API exports/private backups and drift checks remain.

**Uncertainty behavior:** if a named lovelace shadows the import object or its
configuration is inaccessible, the supported APIs used here cannot establish this
read-only import proof. The command stops with that exact blocker and performs no
list/import/write. A supported non-mutating route would require independently bound
evidence that the existing resource collection is already loaded, or the actual
default import source has no legacy key; the current APIs do not expose a loaded
flag. Opening Resources to force loading, editing storage, assuming migration ran,
or accepting a current target config as the legacy source is not a resolution.
No such extra evidence is assumed or demanded in advance: the single corrected
operator command evaluates the supported proof once and stops if unavailable.

**Unchanged boundaries:** existing credential-only normal internal authentication
and actual admin check are repeated only because a fresh single combined API session
requires authentication; accepted auth is not reopened as an investigation. No
filesystem requalification. Absent integration remains inactive; the native delivery
ready flag stays false. Fresh cross-host disabled/exclusive/local route guards,
real mTLS/assertion/private-file/SPKI/independent ACL trust and backups remain mandatory
before any future delivery. No secret provisioning/disclosure, service, runtime,
production, migration, editing/evaluation/notifications/activation or PE-7.4 permission.

**Focused native validation:** documented bundled Windows interpreter, repository
root, shell-free PATH, HIOC_TEST_SHELL cleared, sys.path[:0]=['tests','pi4/lib'].
Final73 tests run,73 passed,0 failures,0 errors,0 skipped,0 class-level skips, exact
final source/test hashes unchanged during run. A preceding73/73 run validated the
same behavior before receipt output was narrowed to HIOC-only resource conflicts;
the final run covers those exact final bytes. Existing104 delivery passes retain
unchanged source/test evidence; no unrelated historical suite or production checks.
Tests cover the config-less/null/missing compatibility panel, actual source success,
config_not_found versus successful null, every legacy-key shape, named alias, unknown
catalog, fixed/missing/duplicate/YAML target, exactly six preserved views, no alternate
config reads, old shape diagnostics, generated/incompatible views, resource conflicts,
all used read failures, credential/privacy protection, no mutation and native guards.

**Independent focused acceptance:** actual source/diff and tests inspected beyond
counts. Panel removal is replaced by the source-supported same-object/alias/key proof;
the list call remains strictly downstream of it. The target is fixed in requests
and receipt; neither missing/incompatible target nor schema error offers fallback.
No publication changes to accepted controller, HA publisher, native transaction/
recovery or trust algorithms. No material repository acceptance blocker remains;
runtime resource qualification is still pending operator evidence.

- `tools/pe73_ha_live_qualify.py`: SHA-256 `ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845`.
- `tests/test_pe73_ha_live_qualify.py`: SHA-256 `728e00d1138e8ea8985a528b87250621e76ec5ad0735e15fba80e52fb6cb7272`.

**Governance and preservation:** exactly five existing paths change: qualifier/tests,
Master Plan, append-only implementation evidence and candidate record. The record's
two existing current-document SHA/blob bindings now bind the exclusive-interface
directive and evidence; no new governance record/model or historical field changes.
All39 current successor and449 unchanged protected identities verify. All13 immutable
PI3 delivery and six immutable HA source identities remain.496 other tracked files,
original contract/amendment, executive authorization quote, PI3 deployment, filesystem
PASS and previous receipts/limitations remain unchanged. Stash preserved. Publication
does not authorize installation or advance PE-7.4.

One next action: run the single immutable-source-verified read-only qualifier on
PI5 Terminal for hioc-dashboard-v2 and resource conflict evidence; retain receipt/
immediate exit status and stop. No Dashboard-selection task or automatic follow-on.

Primary support reviewed:
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/__init__.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/websocket.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/resources.py
- https://github.com/home-assistant/core/blob/2026.10.4/homeassistant/components/lovelace/dashboard.py

### PE-7.3 native trust and guarded HA delivery bindings

Classification: CURRENT REPOSITORY IMPLEMENTATION; PE73 IN_PROGRESS; PE74 NOT_AUTHORIZED.
Baseline 3c561f83f03c4b954bbc23be60a334b0633c0f69, synchronized clean main before work.
This is implementation readiness, not production installation, trust provisioning or
feature activation. No Codex PI3/PI5 access, SSH, credentials or production execution.

**Accepted production evidence (OPERATOR_SUPPLIED, retained):** PI3 guarded artifact
deployment PASS; PI5 filesystem identity qualification PASS; authenticated HA API,
exclusive Dashboard and six view configurations PASS; storage resource inventory11,
zero editor conflicts and legacy resource-import safeguard PASS. Accepted HIOC
Dashboard canonical SHA256 is
7502a36014253a6cce6b5bcd82277c3c59242d33a191161500d5b3f8c6660ab8.
No additional production observations or health/completion claims are invented.
These establish accepted historical qualification, not a reusable exclusive lease.
Fresh checks below are delivery-time continuity requirements, not a broad re-review.

**Owner UI decision:** all manual Asset/device controls belong in existing
hioc-dashboard-v2 / hioc-v2-inventory. A minimal additional grid section/card is now
explicitly approved for functionality. Existing cards/sections retain their order;
all six views, paths, layout/navigation and unrelated content remain intact. The
accepted original Dashboard architecture and PE-7 contract remain byte-identical;
this explicit bounded successor placement decision is recorded here, not silently
edited into their historical text. The repository Dashboard YAML is not installed.
Comprehensive visual refinement is a separate deferred future roadmap checkpoint,
not a present blocker, Dashboard replacement, new UI or PE-7.4 authorization.

**Native private trust:** tools/pe73_ha_production.py supplies PrivateFiles, TrustSide,
the finite Peer/GuardServer channel, NativeHAState/NativeBackendState, DeliveryAPI,
RouteProbe and native_delivery. It reuses Delivery and the existing descriptor
publisher, plus the protected PI3 NativeFS/process observer; no second deployment
transaction, new broker, persistent service, shell or product runtime is introduced.
All imported tooling must come from one verified immutable published toolkit. The
library contains no installation-on-import, auto-start, active configuration writer,
credential generation, Asset-state write or HA/HIOC runtime import.

PrivateFiles opens every ancestor with directory descriptors and NOFOLLOW, verifies
no group/other write, expected root/role ownership and no POSIX ACLs. Its explicitly
approved private parent must already be0700 with the actual role UID/GID. Regular
single-link files must be0600, bounded, owned by that role, with named/descriptor
identity checked before/after reading and while TLS loads the held descriptors via
/proc/self/fd. PI5 owner comes from actual qualified Core identity, not PI3's1000
policy. Missing/unsafe parents are a named provisioning prerequisite, never repaired
or created implicitly in production. PrivateFiles.provision imports only explicitly
supplied already-issued bytes into NEW exclusive files, with bounded writes, fsync,
parent fsync and exact readback; no overwrite, retry, key generation or permissions
repair. The exclusive descriptor alone may be set0600. Uncertain evidence remains.

TrustSide reads a canonical inactive packet through native_packet/PrivateFiles from
each independently owned private trust parent. HA contract paths remain /config;
the Terminal mapping is applied only under the actual shared Core-root proof.
Both packet shapes, all role enable flagsfalse, exact issuer/key ID, private address/
port, HA allowlist and backend exact actor/operation/dev_ID scope are checked using
the accepted disabled_trust validator. Backend packet/ACL is independently read on
PI3, never granted by a HA-supplied assertion or overwritten from the client.
Public/private certificate keys must match. Native cryptography validates bounded
certificate/CA material, time, BasicConstraints, CA signing permission, required
client/server EKU, supplied chain signatures and server IP SAN. OpenSSL, not a new
path-validation algorithm, validates actual peer CA chains during required mutual
TLS >=1.2; client hostname checking stays enabled. Backend verifies exact presented
client SPKI and HA source IP. Addresses/ports must match the inactive runtime plan.
Encrypted/malformed/expired/mismatched/absent material blocks; no password guessing.

The assertion material is exactly32 bytes shared HMAC-SHA256, not an asymmetric
assertion keypair. A domain-separated nonce/session/counter-bound key-possession
proof inside mTLS establishes the pair without sending keys. It is guard evidence
ONLY: no actor assertion, editing command or substitute product protocol. Existing
product message/signature/expiry/replay/ACL semantics and payload remain unchanged.
No raw key, token, sensitive ACL, private path or native exception is returned in
sanitized receipts. Private identities remain inside the authenticated guard channel
and private transaction context, not public readiness reports.

**Finite live guard:** an operator may bind an explicitly approved temporary private
observer port, distinct from the still-disabled product adapter endpoint, using the
existing accepted server certificate/client CA. serve_guard handles exactly one
foreground mTLS connection, at most128 CHECKs over900 seconds, bounded frames,
handshake/read/accept timeouts, exact HA peer IP and client SPKI. There is no daemon,
service installer, arbitrary command/path request, SSH tunnel or mutation/recovery
command. Native role-owned canonical packet readers and the real qualified Supervisor
Proxy/socket are required by production factories; fixture callbacks and
JSON receipts cannot be admitted there. Socket closure never restores cron, changes
consumers, deletes leases or claims delivery success. Unexpected loss fails the
transaction; no reconnection or request/mutation retry.

Both sides generate a fresh random session under the same whole-process reference.
The backend and HA acquire the same fixed lease basename in their approved private
trust parents using exclusive durable create. Existing lease, changed lease, boot,
context, material or deadline refuses. Leases remain for explicit disposition after
failure/uncertainty, not timeout cleanup. A live socket challenge prevents replay of
historical reports. NativeBackendState rereads actual target/boot, exact restored
scheduler SHA, absence of PE-7 scheduled roles, accepted known-process/drain evidence,
all13 installed immutable payload/security identities, and inactive PE-7 evaluator/
notification policy. NativeHAState rereads actual Core/root/namespace/ancestry/device/
inode/owner/mode/ACL, exact approved frontend/public implementation hashes and lease.
Expected host/source bindings are operator-approved accepted observations, never
arbitrary version guesses or a permanent HA version pin.

Manual/independent callers remain PROCEDURALLY prohibited, not universally enforced;
retained descriptors, cached modules and uncooperative/privileged callers are not
claimed excluded. The accepted residual-risk model and whole-process executive
instruction remain verbatim in their prior records. No per-operation approvals are
introduced. Any new unexpected recovery/changed scope retains its separate boundary.
This HA-only transaction does not pause/redeploy PI3, modify its restored cron or
reinterpret its completed artifact deployment as a new maintenance installation.

Bindings verifies actual live peer trust, Core components/services absent, storage
mode and resource availability. DeliveryAPI reuses the qualified Supervisor WebSocket
transport; it does not widen the published read-only qualifier. Resource reads first
repeat ONLY the necessary delivery-time complete-catalog/default-object legacy
import check. Unknown/legacy/shadowed/failed source refuses before resources/list.
The first live HIOC config must match the accepted hash and exact six paths; initial
resource count must remain11. Actual full current exports become the exact private
baseline checked through the transaction. No unrelated Dashboard config is read.
Only the two existing supported resource/create and fixed HIOC config/save writes
are admitted, once each, with exact durable journal intent/whole-process reference,
verified route and exact intended body. Lost ACK consumes the attempt and stops.
No call_service, activation, direct .storage edit, reload, restart or migration API.

**Publication order:** prove the supported www/local mapping and actual destination
before prepare; preserve private exact Dashboard/resource exports and file backups;
publish/read back all four pinned HA files and metadata via existing transaction;
record VERIFYING_LOCAL_RESOURCE; perform bounded credential-free GET of exactly
/local/hioc-asset-editor.js at the explicitly approved HA HTTPS origin, with TLS CA/
hostname verification, actual approved PI5 peer address, no redirects/compression and
exact immutable SHA256; record LOCAL_ROUTE_VERIFIED; only then resource/create and
additive Inventory save. Final independent file/API/route readback is required before
DELIVERED_DISABLED. No absent-file route is claimed served by historical evidence.
Route failure before API mutation records LOCAL_ROUTE_BLOCKED and preserves the four
verified files/backups. Explicit separately adjudicated file recovery is permitted
only with unchanged installed identities and exact original live API baselines.
Journal-save uncertainty retains prior pending intent and prevents unsafe recovery.
Failure after possible API mutation remains nonterminal; no automatic API rollback,
file restore, scheduler restoration, consumer release or retry.

**Operator-specific bindings still required, not fabricated:** approved issued CA/
client/server chains/private keys, shared32-byte HMAC, issuer/key ID, exact independently
owned ACL and HA allowlist, approved private parent paths/observed owners, backend
IP/product port, actual HA source, temporary observer port, actual verified HTTPS
frontend origin/CA, accepted native host/source bindings, and fresh exclusive/manual
responsibility. Runtime constructors/checkers accept these inputs and fail closed;
they are not deployment-ready until bound locally and validated on the actual hosts.
No secret values belong in chat or Git. Native cryptography/proc/ACL capabilities
must be available; the existing product already uses cryptography, but Windows
availability is not asserted as PI3/PI5 observation. No packages are installed here.
requirements() / --requirements is a sanitized, read-only input report, not an
installer or a production qualification. No executable installation command with
invented endpoints, private package or authority is provided.

**Focused final-byte validation and acceptance:** established bundled Windows Python,
repository root, shell-free PATH, HIOC_TEST_SHELL cleared, sys.path setup tests/pi4/lib,
-B. Exactly207 tests run/pass,0 failures/errors/skips/class-level skips. Tests include
real Windows loopback OpenSSL mutual TLS and invalid CA/hostname/missing client;
certificate validity/identity/key/SPKI, HMAC length/pair/drift, ACL, private descriptor/
owner/mode/ancestor/ACL/hard-link/security, finite live challenge/independent packet,
replay/loss/expiry, native boot/cron/process/payload/config drift, fixed lease and
fixture-admission refusals; route timing/bytes/redirect/encoding/peer checks;
Inventory six-view preservation, supported API and legacy safeguard, disabled roles,
full existing-transaction/live-peer integration, interruption and explicit recovery.
Windows POSIX metadata fixtures and socketpair protocol seams are explicitly synthetic;
loopback TLS is real Windows TLS, not Linux or production qualification. No unrelated
historical suites or previously passed production checks are repeated.
Actual source/test logic and negative paths were inspected against the governing
contract independently of the previous readiness summary. Acceptance applies only
to parameterized repository bindings; no external human review, PKI issuance,
native deployment success or production installation is inferred from these tests.

Accepted final implementation/test identities:
- `tools/pe73_ha_delivery.py`: SHA-256 `25ab8ca4140b9ddc73b60f8e921b426a234901ab6634d2239f865469505558ca`.
- `tests/test_pe73_ha_delivery.py`: SHA-256 `832e910008d7dc8497b444f079607ab7c5e3990f4795b6f9d46b3f3f73960584`.
- `tools/pe73_ha_production.py`: SHA-256 `86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c`.
- `tests/test_pe73_ha_production.py`: SHA-256 `116bdfe6fa80912fce9c9e4cb6966cfccd61c1c86aff0f476777e62254323acb`.

All13 PI3 payload, six immutable HA sources,39 successor and449 protected bindings
verify; only the two current documentation entries in the existing candidate record
are refreshed. Original contract, maintenance amendment, controller/provider, runtime
payloads, prior production receipts and historical evidence remain unchanged. Existing
PI3 deployment remains complete. HA/PE-7 integration and all editing/evaluator/
migration/notification/recurring roles remain disabled; no service reload/restart.
Implementation readiness PASS does not mean production delivery readiness. Exactly
one next action: bind the genuine local operator-specific production trust/endpoint
inputs from approved existing material, without secrets in chat or a new discovery
phase. PE73 IN_PROGRESS; PE74 NOT_AUTHORIZED; Codex production access/mutation NONE.

### PE-7.3 offline CA and disabled trust provisioning

Classification: CURRENT PREPARATION; PE73 IN_PROGRESS; PE74 NOT_AUTHORIZED.
Baseline 686be8841f461eacd57a9076948acf632bbf7bea. The owner selected:
**"Create a dedicated offline PE-7 CA locally on PI3".** This authorizes the
bounded local issuance route, not a CA service, global CA trust or PE-7 activation.
No Codex production access or production provisioning occurred.

**Decision boundaries.** The actual private basename, two distinct reserved
unprivileged ports, explicitly approved .252 backend/.251 source addresses,
certificate subjects and validity, existing HTTPS frontend origin, genuine human
HA ID and independently owned exact Asset/operation scope must be entered locally.
No wildcard ACL, system discovery principal substituted for a human, assumed port,
default credential package or pre-approved listener is inferred. The wizard generates
the explicitly new issuer UUID/key ID internally; it does not ask for challenge copying.
These are policy inputs, not separate consequential-operation authorization prompts.
Current interface/source routing and permitted temporary observer reachability still
require actual local verification; no firewall change is authorized or performed here.

**Key custody.** PI3 creates a P-256 offline CA with an encrypted PKCS8 key and a
separate server key; a locally retained passphrase of at least16 bytes is required.
PI5 generates and retains its own client key and sends only its signed CSR. PI3 checks
exact subject/IP SAN/key type/extensions before issuance. Leaves have exact server/client
EKU, validated chain, time and key pairing. The CA and backend private keys never leave
PI3; the HA private key never leaves PI5. The 32-byte random HMAC and inactive packet
transfer only over an existing strict-host-key, batch-authenticated SSH pipe. No keys,
tokens, ACL entries or private transfer bytes appear in public receipts or Git.
The CA file is encrypted at rest, offline from all listeners; no CA daemon or global
trust installation. It must not be treated as a general-purpose PKI or automatic rotation.

**Filesystem and interruptions.** Reuse existing qualified native filesystem and
PrivateFiles reader/provisioner. Only one new direct-child private directory per host
is created, mode0700, role-derived owner (PI3 1000:1000; HA qualified Core identity,
not a PI3 UID assumption). Existing directories/credentials refuse mutation. Native
no-follow ancestry, identity, link, ACL, owner/mode and durable readback checks remain.
Private files0600, complete canonical packet written LAST. There is no second journal,
publisher or recovery algorithm. Partial material and an incomplete toolkit are retained;
stop and preserve evidence, never blindly repeat a mutating step or delete/recover it.

**Dependencies and transport.** Actual PI3/PI5 dependency support is UNKNOWN until
observed. The first action below is read-only PI5 assessment: Terminal Python/OpenSSL,
required cryptography APIs, existing OpenSSH availability and public PI3 known-host
record, plus a fixed import-only Core crypto probe. No HA import/reload, config/secret
read, package install or Core modification. Probe results are not proof of usable SSH
authentication, network policy, listener approval or current filesystem qualification.
Missing crypto, SSH trust/authentication or permission is a BLOCKED prerequisite; no
credential creation, unsafe host-key acceptance or alternative transport is attempted.
If Terminal crypto is missing but Core supports it, the smallest candidate remedy is
a separately reviewed temporary Terminal-only dependency bundle pinned for the observed
Python/architecture, not installing into Core/global packages. Its feasibility and exact
wheel identities are not established by Windows tests and are not invented here.

**Validation.** 48/48 focused native Windows tests, zero failures/errors/skips:
new CA randomness/encryption, SAN/EKU/pair/time/chain, actual OpenSSL mutual TLS over
Windows loopback using newly issued material, policy/ACL negatives, partial/collision
handling, two-host private transfer fixtures, wrong pin/key/plan and stale HMAC refusal,
dependency refusal and redacted receipts. Synthetic NativePacket adapters in fixture
tests are explicitly not production evidence; the unchanged native factory still rejects
fixture readers. Existing 207 binding tests remain tied to unchanged accepted source;
their owner/mode/ACL/symlink, guard, native type and transaction results are retained.
No live Pi mTLS, HMAC possession, source-IP policy, credential installation or endpoint
readiness is claimed. Independent exact-byte source inspection retains all native gates.

**Direct delivery continuity.** The final canonical packet is consumed by unchanged
NativePacket and TrustSide; exact source/runtime paths and independently owned ACL are
preserved. Actual connect_peer/serve_guard key possession, approved-source identity,
NativeHAState/NativeBackendState leases and native_delivery requirements remain mandatory
in the existing delivery session. Do not start an isolated guard merely as a test: its
durable one-attempt lease cannot be discarded or reused. Provisioning itself opens no
application or guard listener and performs no filesystem installation or HA API mutation.
The existing Delivery alone publishes four artifacts, verifies actual editor route bytes
before resource registration, then appends only the minimal Inventory section. No `.storage`
edit, alternative Dashboard, reload/restart, PE-7 editing/evaluation/migration/notification
or recurring activation. Preserve all six HIOC views and accepted PI3 evidence.

**Deterministic operator sequence — stop after each receipt; no automatic retries.**

1. PI5 HA: read-only provisioning-runtime assessment supplied in the handoff. If a
   prerequisite is BLOCKED, stop before the mutating steps; report only its sanitized receipt.
2. PI3 NUT&PIHOLE as jazofv1: prepare the dedicated offline CA/server material. Mutating
   only a new private toolkit cache and approved private trust child; requires local explicit
   policy values and masked CA passphrase. Expected PASS_BACKEND_OFFLINE_CA_PREPARATION.
3. PI5 Terminal: create its local client key/CSR and transfer only the public CSR using
   existing SSH trust/authentication. Mutating new approved HA trust child only. Expected
   PASS_HA_LOCAL_KEY_AND_PUBLIC_REQUEST. No private key crosses hosts.
4. PI3: unlock the offline CA locally for the exact saved CSR. Expected
   PASS_BACKEND_OFFLINE_ISSUANCE; encrypted CA/private backend key retained only on PI3.
5. PI5: securely pull and validate the completed inactive bundle, compare transferred
   HMAC to protected local readback; expected PASS_HA_DISABLED_TRUST_PROVISIONING with
   cross_host_live_validation=REQUIRED. Local PASS is not live trust or deployment PASS.
6. Existing guarded delivery session, only after actual prerequisites are established:
   use the same packets/private paths in actual TrustSide/NativePacket, bounded observer,
   fresh leases, authenticated_proxy and native_delivery. Actual mutual TLS verifies
   chain/hostname/client SPKI/source IP and fresh HMAC key possession. All current source,
   scheduler, disabled-state and route gates remain; no fabricated host identity or
   capability hash. This preparation does not authorize arbitrary inputs or publish a
   speculative installation command before those mandatory native facts exist.

The following complete commands implement steps2–5 without manual source editing,
hash copying or operation identifiers. The content hash pins the new helper even if
the public main moves; dependencies remain pinned to accepted baseline686be884.
They use existing HTTPS CA verification and existing SSH identity only, never sudo,
credentials in arguments or global package installation. The cache is code only, not
a secret store. An existing exact cache is read/verified; a partial/different one stops.
No cryptographic material is printed by ordinary actions; `_pipe` is internal SSH-only
transport, never an operator command or user-visible output channel.

**PI3 — backend-init**

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,os,pathlib,stat,sys,urllib.request
PINS={'pe73_ha_production': '86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c', 'pe73_ha_delivery': '25ab8ca4140b9ddc73b60f8e921b426a234901ab6634d2239f865469505558ca', 'pe73_ha_assess': 'da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443', 'pe73_ha_live_qualify': 'ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845', 'pe73_maintenance_window': '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741', 'hioc-pe73-pi3-delivery': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2'}
EXPECTED='2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
ACTION='backend-init'
try:
    if sys.platform!='linux' or not (os.getuid()==os.geteuid()==os.getgid()==os.getegid()==1000):
        raise ValueError('TARGET_IDENTITY')
    base='https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/'
    def fetch(url,identity):
        with urllib.request.urlopen(url,timeout=30) as stream:
            raw=stream.read(1048577)
        if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!=identity:raise ValueError('SOURCE_IDENTITY')
        return raw
    raw=fetch(base+'main/tools/pe73_ha_provision.py',EXPECTED)
    # Actual crypto APIs must exist BEFORE cache or credential writes.
    scope={'__name__':'pe73_bootstrap_check','__file__':'verified-memory-source'}
    exec(compile(raw,'verified-memory-source','exec'),scope);scope['crypto']()
    root=pathlib.Path.home()/'.hioc-pe73-provision-toolkit'
    home=root.parent.lstat()
    if not stat.S_ISDIR(home.st_mode) or home.st_uid!=1000 or stat.S_IMODE(home.st_mode)&0o022:raise ValueError('HOME_SECURITY')
    sources={'pe73_ha_provision.py':raw}
    for name,identity in PINS.items():
        sources[name+'.py']=fetch(base+'686be8841f461eacd57a9076948acf632bbf7bea/tools/'+name+'.py',identity)
    # Existing exact toolkit can be read again; partial/mismatched caches STOP.
    new=not os.path.lexists(root)
    if new:os.mkdir(root,0o700)
    info=root.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=1000 or stat.S_IMODE(info.st_mode)!=0o700:raise ValueError('CACHE_SECURITY')
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        if (info.st_dev,info.st_ino)!=(os.fstat(fd).st_dev,os.fstat(fd).st_ino):raise ValueError('CACHE_IDENTITY')
        for acl in ('system.posix_acl_access','system.posix_acl_default'):
            try:os.getxattr(fd,acl)
            except OSError as error:
                import errno
                if error.errno!=errno.ENODATA:raise
            else:raise ValueError('CACHE_ACL')
        if not new and set(os.listdir(fd))!=set(sources):raise ValueError('PARTIAL_CACHE')
        for name,value in sources.items():
            flags=os.O_RDWR|os.O_NOFOLLOW|(os.O_CREAT|os.O_EXCL if new else 0)
            item=os.open(name,flags,0o600,dir_fd=fd)
            try:
                obj=os.fstat(item)
                if not stat.S_ISREG(obj.st_mode) or obj.st_uid!=1000 or obj.st_nlink!=1 or stat.S_IMODE(obj.st_mode)!=0o600:raise ValueError('SOURCE_SECURITY')
                if new:
                    with os.fdopen(os.dup(item),'wb') as stream:stream.write(value);stream.flush();os.fsync(stream.fileno())
                os.lseek(item,0,os.SEEK_SET)
                if os.read(item,1048577)!=value:raise ValueError('SOURCE_READBACK')
            finally:os.close(item)
        os.fsync(fd)
    finally:os.close(fd)
    sys.argv=[str(root/'pe73_ha_provision.py'),ACTION]
    exec(compile(raw,str(root/'pe73_ha_provision.py'),'exec'),{'__name__':'__main__','__file__':str(root/'pe73_ha_provision.py')})
except BaseException as error:
    if isinstance(error,SystemExit):raise
    print(json.dumps({'RESULT':'BLOCKED_PROVISIONING_BOOTSTRAP','partial_material':'RETAINED_IF_CREATED','automatic_retry':False,'STOP_REQUIRED':True},sort_keys=True))
    raise SystemExit(1)
PY
pe73_status=$?
printf 'PE73_PROVISION_EXIT_STATUS=%s\n' "$pe73_status"
```

**PI5 — ha-request**

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,os,pathlib,stat,sys,urllib.request
PINS={'pe73_ha_production': '86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c', 'pe73_ha_delivery': '25ab8ca4140b9ddc73b60f8e921b426a234901ab6634d2239f865469505558ca', 'pe73_ha_assess': 'da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443', 'pe73_ha_live_qualify': 'ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845', 'pe73_maintenance_window': '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741', 'hioc-pe73-pi3-delivery': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2'}
EXPECTED='2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
ACTION='ha-request'
try:
    if sys.platform!='linux' or not (os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0):
        raise ValueError('TARGET_IDENTITY')
    base='https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/'
    def fetch(url,identity):
        with urllib.request.urlopen(url,timeout=30) as stream:
            raw=stream.read(1048577)
        if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!=identity:raise ValueError('SOURCE_IDENTITY')
        return raw
    raw=fetch(base+'main/tools/pe73_ha_provision.py',EXPECTED)
    # Actual crypto APIs must exist BEFORE cache or credential writes.
    scope={'__name__':'pe73_bootstrap_check','__file__':'verified-memory-source'}
    exec(compile(raw,'verified-memory-source','exec'),scope);scope['crypto']()
    root=pathlib.Path.home()/'.hioc-pe73-provision-toolkit'
    home=root.parent.lstat()
    if not stat.S_ISDIR(home.st_mode) or home.st_uid!=0 or stat.S_IMODE(home.st_mode)&0o022:raise ValueError('HOME_SECURITY')
    sources={'pe73_ha_provision.py':raw}
    for name,identity in PINS.items():
        sources[name+'.py']=fetch(base+'686be8841f461eacd57a9076948acf632bbf7bea/tools/'+name+'.py',identity)
    # Existing exact toolkit can be read again; partial/mismatched caches STOP.
    new=not os.path.lexists(root)
    if new:os.mkdir(root,0o700)
    info=root.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=0 or stat.S_IMODE(info.st_mode)!=0o700:raise ValueError('CACHE_SECURITY')
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        if (info.st_dev,info.st_ino)!=(os.fstat(fd).st_dev,os.fstat(fd).st_ino):raise ValueError('CACHE_IDENTITY')
        for acl in ('system.posix_acl_access','system.posix_acl_default'):
            try:os.getxattr(fd,acl)
            except OSError as error:
                import errno
                if error.errno!=errno.ENODATA:raise
            else:raise ValueError('CACHE_ACL')
        if not new and set(os.listdir(fd))!=set(sources):raise ValueError('PARTIAL_CACHE')
        for name,value in sources.items():
            flags=os.O_RDWR|os.O_NOFOLLOW|(os.O_CREAT|os.O_EXCL if new else 0)
            item=os.open(name,flags,0o600,dir_fd=fd)
            try:
                obj=os.fstat(item)
                if not stat.S_ISREG(obj.st_mode) or obj.st_uid!=0 or obj.st_nlink!=1 or stat.S_IMODE(obj.st_mode)!=0o600:raise ValueError('SOURCE_SECURITY')
                if new:
                    with os.fdopen(os.dup(item),'wb') as stream:stream.write(value);stream.flush();os.fsync(stream.fileno())
                os.lseek(item,0,os.SEEK_SET)
                if os.read(item,1048577)!=value:raise ValueError('SOURCE_READBACK')
            finally:os.close(item)
        os.fsync(fd)
    finally:os.close(fd)
    sys.argv=[str(root/'pe73_ha_provision.py'),ACTION]
    exec(compile(raw,str(root/'pe73_ha_provision.py'),'exec'),{'__name__':'__main__','__file__':str(root/'pe73_ha_provision.py')})
except BaseException as error:
    if isinstance(error,SystemExit):raise
    print(json.dumps({'RESULT':'BLOCKED_PROVISIONING_BOOTSTRAP','partial_material':'RETAINED_IF_CREATED','automatic_retry':False,'STOP_REQUIRED':True},sort_keys=True))
    raise SystemExit(1)
PY
pe73_status=$?
printf 'PE73_PROVISION_EXIT_STATUS=%s\n' "$pe73_status"
```

**PI3 — backend-issue**

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,os,pathlib,stat,sys,urllib.request
PINS={'pe73_ha_production': '86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c', 'pe73_ha_delivery': '25ab8ca4140b9ddc73b60f8e921b426a234901ab6634d2239f865469505558ca', 'pe73_ha_assess': 'da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443', 'pe73_ha_live_qualify': 'ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845', 'pe73_maintenance_window': '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741', 'hioc-pe73-pi3-delivery': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2'}
EXPECTED='2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
ACTION='backend-issue'
try:
    if sys.platform!='linux' or not (os.getuid()==os.geteuid()==os.getgid()==os.getegid()==1000):
        raise ValueError('TARGET_IDENTITY')
    base='https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/'
    def fetch(url,identity):
        with urllib.request.urlopen(url,timeout=30) as stream:
            raw=stream.read(1048577)
        if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!=identity:raise ValueError('SOURCE_IDENTITY')
        return raw
    raw=fetch(base+'main/tools/pe73_ha_provision.py',EXPECTED)
    # Actual crypto APIs must exist BEFORE cache or credential writes.
    scope={'__name__':'pe73_bootstrap_check','__file__':'verified-memory-source'}
    exec(compile(raw,'verified-memory-source','exec'),scope);scope['crypto']()
    root=pathlib.Path.home()/'.hioc-pe73-provision-toolkit'
    home=root.parent.lstat()
    if not stat.S_ISDIR(home.st_mode) or home.st_uid!=1000 or stat.S_IMODE(home.st_mode)&0o022:raise ValueError('HOME_SECURITY')
    sources={'pe73_ha_provision.py':raw}
    for name,identity in PINS.items():
        sources[name+'.py']=fetch(base+'686be8841f461eacd57a9076948acf632bbf7bea/tools/'+name+'.py',identity)
    # Existing exact toolkit can be read again; partial/mismatched caches STOP.
    new=not os.path.lexists(root)
    if new:os.mkdir(root,0o700)
    info=root.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=1000 or stat.S_IMODE(info.st_mode)!=0o700:raise ValueError('CACHE_SECURITY')
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        if (info.st_dev,info.st_ino)!=(os.fstat(fd).st_dev,os.fstat(fd).st_ino):raise ValueError('CACHE_IDENTITY')
        for acl in ('system.posix_acl_access','system.posix_acl_default'):
            try:os.getxattr(fd,acl)
            except OSError as error:
                import errno
                if error.errno!=errno.ENODATA:raise
            else:raise ValueError('CACHE_ACL')
        if not new and set(os.listdir(fd))!=set(sources):raise ValueError('PARTIAL_CACHE')
        for name,value in sources.items():
            flags=os.O_RDWR|os.O_NOFOLLOW|(os.O_CREAT|os.O_EXCL if new else 0)
            item=os.open(name,flags,0o600,dir_fd=fd)
            try:
                obj=os.fstat(item)
                if not stat.S_ISREG(obj.st_mode) or obj.st_uid!=1000 or obj.st_nlink!=1 or stat.S_IMODE(obj.st_mode)!=0o600:raise ValueError('SOURCE_SECURITY')
                if new:
                    with os.fdopen(os.dup(item),'wb') as stream:stream.write(value);stream.flush();os.fsync(stream.fileno())
                os.lseek(item,0,os.SEEK_SET)
                if os.read(item,1048577)!=value:raise ValueError('SOURCE_READBACK')
            finally:os.close(item)
        os.fsync(fd)
    finally:os.close(fd)
    sys.argv=[str(root/'pe73_ha_provision.py'),ACTION]
    exec(compile(raw,str(root/'pe73_ha_provision.py'),'exec'),{'__name__':'__main__','__file__':str(root/'pe73_ha_provision.py')})
except BaseException as error:
    if isinstance(error,SystemExit):raise
    print(json.dumps({'RESULT':'BLOCKED_PROVISIONING_BOOTSTRAP','partial_material':'RETAINED_IF_CREATED','automatic_retry':False,'STOP_REQUIRED':True},sort_keys=True))
    raise SystemExit(1)
PY
pe73_status=$?
printf 'PE73_PROVISION_EXIT_STATUS=%s\n' "$pe73_status"
```

**PI5 — ha-complete**

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,os,pathlib,stat,sys,urllib.request
PINS={'pe73_ha_production': '86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c', 'pe73_ha_delivery': '25ab8ca4140b9ddc73b60f8e921b426a234901ab6634d2239f865469505558ca', 'pe73_ha_assess': 'da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443', 'pe73_ha_live_qualify': 'ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845', 'pe73_maintenance_window': '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741', 'hioc-pe73-pi3-delivery': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2'}
EXPECTED='2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
ACTION='ha-complete'
try:
    if sys.platform!='linux' or not (os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0):
        raise ValueError('TARGET_IDENTITY')
    base='https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/'
    def fetch(url,identity):
        with urllib.request.urlopen(url,timeout=30) as stream:
            raw=stream.read(1048577)
        if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!=identity:raise ValueError('SOURCE_IDENTITY')
        return raw
    raw=fetch(base+'main/tools/pe73_ha_provision.py',EXPECTED)
    # Actual crypto APIs must exist BEFORE cache or credential writes.
    scope={'__name__':'pe73_bootstrap_check','__file__':'verified-memory-source'}
    exec(compile(raw,'verified-memory-source','exec'),scope);scope['crypto']()
    root=pathlib.Path.home()/'.hioc-pe73-provision-toolkit'
    home=root.parent.lstat()
    if not stat.S_ISDIR(home.st_mode) or home.st_uid!=0 or stat.S_IMODE(home.st_mode)&0o022:raise ValueError('HOME_SECURITY')
    sources={'pe73_ha_provision.py':raw}
    for name,identity in PINS.items():
        sources[name+'.py']=fetch(base+'686be8841f461eacd57a9076948acf632bbf7bea/tools/'+name+'.py',identity)
    # Existing exact toolkit can be read again; partial/mismatched caches STOP.
    new=not os.path.lexists(root)
    if new:os.mkdir(root,0o700)
    info=root.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=0 or stat.S_IMODE(info.st_mode)!=0o700:raise ValueError('CACHE_SECURITY')
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        if (info.st_dev,info.st_ino)!=(os.fstat(fd).st_dev,os.fstat(fd).st_ino):raise ValueError('CACHE_IDENTITY')
        for acl in ('system.posix_acl_access','system.posix_acl_default'):
            try:os.getxattr(fd,acl)
            except OSError as error:
                import errno
                if error.errno!=errno.ENODATA:raise
            else:raise ValueError('CACHE_ACL')
        if not new and set(os.listdir(fd))!=set(sources):raise ValueError('PARTIAL_CACHE')
        for name,value in sources.items():
            flags=os.O_RDWR|os.O_NOFOLLOW|(os.O_CREAT|os.O_EXCL if new else 0)
            item=os.open(name,flags,0o600,dir_fd=fd)
            try:
                obj=os.fstat(item)
                if not stat.S_ISREG(obj.st_mode) or obj.st_uid!=0 or obj.st_nlink!=1 or stat.S_IMODE(obj.st_mode)!=0o600:raise ValueError('SOURCE_SECURITY')
                if new:
                    with os.fdopen(os.dup(item),'wb') as stream:stream.write(value);stream.flush();os.fsync(stream.fileno())
                os.lseek(item,0,os.SEEK_SET)
                if os.read(item,1048577)!=value:raise ValueError('SOURCE_READBACK')
            finally:os.close(item)
        os.fsync(fd)
    finally:os.close(fd)
    sys.argv=[str(root/'pe73_ha_provision.py'),ACTION]
    exec(compile(raw,str(root/'pe73_ha_provision.py'),'exec'),{'__name__':'__main__','__file__':str(root/'pe73_ha_provision.py')})
except BaseException as error:
    if isinstance(error,SystemExit):raise
    print(json.dumps({'RESULT':'BLOCKED_PROVISIONING_BOOTSTRAP','partial_material':'RETAINED_IF_CREATED','automatic_retry':False,'STOP_REQUIRED':True},sort_keys=True))
    raise SystemExit(1)
PY
pe73_status=$?
printf 'PE73_PROVISION_EXIT_STATUS=%s\n' "$pe73_status"
```

Accepted source identities:
- `tools/pe73_ha_provision.py`: SHA-256 `2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89`.
- `tests/test_pe73_ha_provision.py`: SHA-256 `63ac73a9bfcb63e4fe1a1427ddabd5f08ea7533499211c63ea290cc565559e49`.

### PE-7.3 Terminal-only pinned provisioning environment

Classification: CURRENT REPOSITORY CORRECTION; PE73 IN_PROGRESS; PE74 NOT_AUTHORIZED.
Baseline b5a020982484e35126daa70b256860a23af8e88f. No Codex PI3/PI5 access.

**New OPERATOR_SUPPLIED PI5 receipt, preserved:**
RESULT=BLOCKED_TERMINAL_CRYPTOGRAPHY_UNAVAILABLE; EXIT_STATUS=1.
Terminal CPython3.14.8/aarch64, OpenSSL3.5.9; cryptography unavailable.
Core CPython3.14.9 with cryptography50.0.1. SSH and SCP available; PI3 host key
recognized; no credentials read and no production mutation. These are operator
observations, not independent Codex production inspection. Existing SSH authentication
success, libc/native loader compatibility and stdlib venv availability were not proved.

**Root cause and bounded correction:** The preceding bootstrap required crypto()
in Terminal before any isolated dependency setup. That prerequisite is false on the
observed Terminal. Core's successful import does not authorize Core provisioning.
The existing helper and all trust/deployment code remain byte-identical. A finite
Terminal-only environment helper creates exactly one new private root-owned cache at
`/root/.hioc-pe73-provision-environment`, outside the shared HA configuration/runtime.
It uses stdlib venv without ensurepip, system packages, upgrades or global installation;
an absent venv module fails before cache creation. No Docker/Core invocation, container
change, added privileges, service, listener, scheduler, HA/API/resource check or secret
operation. Neither Core's interpreter nor Core's cryptography is used.

**Pinned official dependency closure:** cryptography50.0.2, cffi2.0.0, pycparser2.23;
installer pip25.3 is executed only from its verified wheel, not installed globally.
Metadata and full wheel bytes were independently checked against official PyPI release
SHA256/size and archive tags. Cryptography cp311-abi3 and CFFI cp314-cp314 aarch64
wheels are provided for manylinux2014/glibc>=2.17 and musllinux1.2; pure pycparser and
pip wheels complete the closure for ordinary CPython3.14. Free-threaded Python and
other ABIs/architectures are not silently accepted. No inferred libc from HA OS or
from Core. Official pip uses native compatible tags; unsupported tags stop before
installation. Exact versions/hashes, --no-index, --no-deps, --only-binary=:all:,
--require-hashes, --no-user and an explicit isolated prefix prevent arbitrary resolution,
source builds or host installation. All downloads verify before cache creation.
Installer configuration is disabled; subprocess environments omit Supervisor tokens,
proxy credentials, user Python paths and SSH agents. HTTPS downloads do not use proxy
credentials. Installation is offline; no global package manager or network fallback.

Primary support: [Python3.14 venv](https://docs.python.org/3.14/library/venv.html),
[cryptography wheel support](https://cryptography.io/en/latest/installation/),
[pip secure binary/hash installs](https://pip.pypa.io/en/stable/topics/secure-installs/),
[pip configuration isolation](https://pip.pypa.io/en/stable/topics/configuration/).
Exact release metadata: [cryptography50.0.2](https://pypi.org/pypi/cryptography/50.0.2/json),
[cffi2.0.0](https://pypi.org/pypi/cffi/2.0.0/json),
[pycparser2.23](https://pypi.org/pypi/pycparser/2.23/json),
[pip25.3](https://pypi.org/pypi/pip/25.3/json).

**Security and failure handling:** New cache parent0700, new downloaded sources0600,
exclusive creation, observed role owner0:0 and no-follow/ACL checks. Existing cache
refused; no overwrite, recursive deletion, environment replacement or automatic retry.
Failed preparation retains its partial private cache without a usable ready seal; stop
and preserve that evidence. No attempt is made to delete unknown/replaced files or
to run provisioning after failed qualification. Final marker is written only after
native imports, exact versions, module origins within venv, crypto API availability
and ephemeral in-memory key/CSR smoke succeed. No production credential is generated.
All installed files and the source interpreter are fingerprinted. Each later launch
rechecks the seal, versions and interpreter before allowing only existing ha-request
or ha-complete. Bytecode writes disabled; no permanent runtime dependency is introduced
into HA/HIOC. The standard venv lib64->lib alias is accepted exactly; other links fail.
Do not delete/recreate a failed or drifted environment without explicit recovery scope.

**Trust and runtime continuity:** Seven exact prior helper/dependency sources are
downloaded from their accepted immutable revisions and verified. The HA private key
is generated locally by the unchanged helper inside Terminal, then stored only in its
qualified HA-owned private directory, not transferred to PI3/Windows or receipts.
Offline CA remains encrypted/operated on PI3; HMAC remains exactly32 bytes; no changes
to issuer/independent ACL, mTLS/SPKI, NativePacket/TrustSide, controller, route ordering,
exclusive Dashboard/Inventory, persistent Asset isolation or enable=false semantics.
Only the existing SSH agent socket reference is optionally passed to the later SSH
provisioning action; no application token or private key value is passed by this helper.

**Validation:** 33/33 focused native Windows tests, zero failures/errors/skips, including
actual local venv isolation, missing Terminal crypto/venv, positive isolated sequencing,
hash/length/path/redirect failures, binary-only offline arguments, secret-env isolation,
interruption retention, missing/altered ready seal, no Core command and expected venv
alias handling. Two official pip offline dry runs resolve exactly the pinned three
packages for CPython3.14/cp314 on aarch64 glibc and musl; no target package installation.
The Linux wheels were not executed on Windows. Actual PI5 native-loader/import success
remains UNKNOWN until the operator runs the command below. No production provisioning,
current freshness, cross-host key proof or delivery readiness is claimed from tests.
The earlier 48 provisioning and207 binding test results remain tied to unchanged code.
13 PI3/six HA payload,39 successor/449 protected identities verify; original contracts,
amendment, executive decision and historical receipts preserved. Only the two current
documentation artifact identities are refreshed in existing governance.

**Integrated operator sequence:** The immediate next action is PI5 environment
preparation/qualification only; it creates a private Terminal cache and no credentials.
Expected PASS_PI5_ISOLATED_PROVISIONING_ENVIRONMENT, native_smoke=PASS, exit0.
A BLOCKED receipt stops with no fallback or automatic retry. Then use the existing
PI3 backend-init and backend-issue commands unchanged. For the corresponding PI5
steps3/5, the two commands below supersede the prior system-Python bootstrap: they
verify this environment helper's exact content, recheck the ready seal and execute the
unchanged provisioning helper with isolated Python. No manual hash/context copying,
Core package installation or new authorization prompts. Existing locally approved
identity/endpoint/ACL inputs and authenticated SSH prerequisites still apply.
No repeated filesystem/API/Dashboard/resource qualification here; later actual
credential/delivery-time security gates remain mandatory.

**PI5 HA Terminal — ha-request (only after successful environment qualification and its preceding PI3 step)**

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,sys,urllib.request
url="https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/main/tools/pe73_provision_environment.py"
try:
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url,timeout=30) as response:
        if response.geturl()!=url:raise ValueError()
        raw=response.read(1048577)
    if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!="0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7":raise ValueError()
except Exception:
    print(json.dumps({"RESULT":"BLOCKED_VERIFIED_ENVIRONMENT_SOURCE","STOP_REQUIRED":True}))
    raise SystemExit(1)
sys.argv=["pe73_provision_environment.py","ha-request"]
exec(compile(raw,url,"exec"),{"__name__":"__main__","__file__":url})
PY
pe73_status=$?
printf 'PE73_ISOLATED_ENVIRONMENT_EXIT_STATUS=%s\n' "$pe73_status"
```

**PI5 HA Terminal — ha-complete (only after successful environment qualification and its preceding PI3 step)**

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,sys,urllib.request
url="https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/main/tools/pe73_provision_environment.py"
try:
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url,timeout=30) as response:
        if response.geturl()!=url:raise ValueError()
        raw=response.read(1048577)
    if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!="0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7":raise ValueError()
except Exception:
    print(json.dumps({"RESULT":"BLOCKED_VERIFIED_ENVIRONMENT_SOURCE","STOP_REQUIRED":True}))
    raise SystemExit(1)
sys.argv=["pe73_provision_environment.py","ha-complete"]
exec(compile(raw,url,"exec"),{"__name__":"__main__","__file__":url})
PY
pe73_status=$?
printf 'PE73_ISOLATED_ENVIRONMENT_EXIT_STATUS=%s\n' "$pe73_status"
```

Exact accepted source identities:
- `tools/pe73_provision_environment.py`: SHA256 `0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7`.
- `tests/test_pe73_provision_environment.py`: SHA256 `238acfbe6fb3be93eccc1c80809ae24ae31e3613daa1501c813184a87cce6b30`.

Pinned wheel identities:
- `cryptography-50.0.2-cp311-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl`: SHA256 `79def8d059362e7831389ed3be0ecdf58a89386e1271e35dd9f5af84e81bffd0`.
- `cryptography-50.0.2-cp311-abi3-musllinux_1_2_aarch64.whl`: SHA256 `25784ce8b9621c90c643efb9e1e2162ab3b0224cae446ad5e70e7fcb1ce18b51`.
- `cffi-2.0.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl`: SHA256 `24b6f81f1983e6df8db3adc38562c83f7d4a0c36162885ec7f7b77c7dcbec97b`.
- `cffi-2.0.0-cp314-cp314-musllinux_1_2_aarch64.whl`: SHA256 `737fe7d37e1a1bffe70bd5754ea763a62a066dc5913ca57e957824b72a85e205`.
- `pycparser-2.23-py3-none-any.whl`: SHA256 `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934`.
- `pip-25.3-py3-none-any.whl`: SHA256 `9655943313a94722b7774661c21049070f6bbb0a1516bf02f7c8d5d9201514cd`.

### PE-7.3 PI3 UID1000 isolated provisioning environment

Classification: CURRENT BOUNDED ENVIRONMENT PREPARATION; PE73 IN_PROGRESS;
PE74 NOT_AUTHORIZED. Baseline513d511fe255e11a875145543f62fa5dca2169a1.

**Actual operator evidence (OPERATOR_SUPPLIED, not Codex observation):**
PI3 NUT&PIHOLE: RESULT=BLOCKED_PI3_PROVISIONING_CRYPTO;
PE73_PI3_CRYPTO_EXIT_STATUS=1; Python3.11.2/aarch64; jazofv1 UID1000;
installed cryptography38.0.4 lacks some required APIs; production mutations none.
Separately, the operator confirms PI5's isolated environment has passed production
validation with cryptography50.0.2,cffi2.0.0,pycparser2.23. No additional receipt fields,
GID/home observations or service health results are invented. The PI5 checkpoint is
not repeated, modified or reopened; its exact accepted source remains unchanged.

**Correction and boundary:** A PI3-only role profile loads the accepted environment
engine from immutable commit513d511, SHA256
0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7,
verifies its exact bytes before compilation, and reuses its original finite prepare,
fetch/hash/archive validation, lock generation, pip command and subprocess isolation
algorithms. Role-specific ownership/ancestry/file/seal checks use UID/GID1000 instead
of PI5's root policy; only the private in-memory engine instance changes. The PI5
source file and production environment never change. No new installer, CA mechanism,
trust transport, deployment journal or framework. The original trust/provisioning
helper and all accepted production bindings remain byte-identical.

**Native preconditions:** Require Linux CPython3.11/aarch64, hostname nutandpihole,
real/effective UID/GID1000, account jazofv1 with governed home/home-group. Root execution
is explicitly rejected, not a fallback. Existing stdlib venv must be available;
otherwise stop before environment creation. No apt, sudo, ensurepip, host/user package
installation or source builds. Existing system Python and cryptography38.0.4 are not
imported for dependency setup, upgraded or replaced. No assumptions about current
libc from the machine label; official pip selects compatible native wheel tags.

**Private path and ownership:** Create only the new cache
`/home/jazofv1/.hioc-pe73-provision-environment`, mode0700, outside both
`/home/jazofv1/hioc` and `/home/jazofv1/hioc-release-source`. All ancestors are opened
with no-follow directory descriptors and checked for owner/group, no group/other
writes, no ACLs and named/held device/inode continuity. Home/cache leaf owner must
be1000:1000; allowed root-owned ancestors do not imply root execution. New source/
wheel/receipt files exclusively created0600, owner1000:1000; symlinks, hardlinks,
unexpected ownership, ACL ambiguity and drift fail closed. Only the standard venv
lib64->lib alias is permitted. Existing cache refuses mutation. Interrupted/uncertain
setup retains the private partial cache, creates no usable ready seal, and never
automatically retries, deletes/recreates, provisions credentials or changes services.

**Dependencies:** cryptography50.0.2 (same cp311-abi3 wheels as accepted PI5),
cffi2.0.0 cp311-cp311 aarch64 manylinux2014/glibc>=2.17 or musllinux1.2 wheels,
pycparser2.23 and the existing SHA-pinned pip25.3 wheel. Every URL/size/SHA256 is pinned
and full archive bytes verified before cache creation. Installation is offline,
binary-only, exact-version, hash-required, no dependency resolution or global/user
packages. The accepted engine omits inherited tokens, proxy/SSH credentials and
Python user paths from subprocesses; no secrets or raw subprocess exceptions in
receipts. No OS package or global CA trust changes. Primary support:
[Python3.11 venv](https://docs.python.org/3.11/library/venv.html),
[CFFI2.0.0 release wheels](https://pypi.org/project/cffi/2.0.0/), and the previously
accepted [pip secure install contract](https://pip.pypa.io/en/stable/topics/secure-installs/).
Pins gate this finite provisioning environment, not a permanent HIOC runtime version.
Independently updated dependencies require a new bounded compatibility/pin review.

**Actual API smoke:** Inside isolated Python, require exact versions, origins under
the venv, no system/user site exposure, CSR signing, existing helper crypto() and
native toolkit import, encrypted PKCS8 roundtrip, UTC certificate validity properties,
PEM certificate loading and verify_directly_issued_by. Test only an ephemeral,
self-signed non-CA leaf with an explicit fixture subject; no production CA, production
certificate issuance, trust identity, HMAC provisioning or private-key persistence.
The secret test bytes never enter stdout/receipts. Write ready.json only after full
smoke success and file/interpreter fingerprinting. A native failure never becomes PASS.

**CA custody limit retained, not silently weakened:** This helper exposes only
`prepare`, not backend-init, backend-issue or any credential operation. It creates
and stores no CA material anywhere. Normal HIOC jobs and the operator share UID1000;
0700/0600 alone cannot exclude same-UID runtime processes. Outside-runtime private CA
custody must be established before a later production CA action; the existing
backend-init runtime-parent placement is not accepted as satisfying that requirement.
Do not run that credential command on the strength of this environment result.
No new privileged account/service, CA mechanism or policy change is introduced here.
The dedicated PI3-operated CA and exact32-byte HMAC-SHA256 design remain unchanged;
PI5 client-key generation/custody and independent backend ACL remain mandatory.

**Validation/acceptance:** 33/33 focused PI3 profile tests, zero failures/errors/skips:
exact shared-engine identity, unchanged PI5 source/profile, root/wrong user/group/
host/ABI refusal, complete descriptor ancestry/ACL/drift cases, UID1000 seal owner/mode/
link checks, missing old system crypto, unsupported wheels, partial/interrupted setup,
no ready on incomplete smoke, no credential CLI and actual ephemeral cryptographic
API execution on Windows. Two official offline pip dry runs resolve the exact pinned
closure for CPython3.11/cp311 aarch64 glibc and musl without installing target packages.
These are repository/synthetic results, not actual native PI3 qualification. Full
Linux wheel imports on PI3 remain pending the operator command. The completed PI5
native checkpoint and historical Windows suites are not rerun. All13 PI3/six HA,
39 successor/449 protected identities verified; accepted controller/contracts,
amendment, executive instruction and all historical production evidence preserved.

**Exactly one next operator action:** PI3 NUT&PIHOLE as jazofv1, no sudo: execute the
immutable-source-verified `prepare` command supplied with the publication handoff.
Expected PASS_PI3_ISOLATED_PROVISIONING_ENVIRONMENT, provisioning_crypto_apis=PASS,
native_smoke=PASS and exit0. It only establishes/smoke-tests this private environment.
On BLOCKED/interruption stop, retain evidence, do not retry or remove the cache.
No CA/key issuance, HMAC material, HIOC mutation, activation or PI5 operation.
PE73 remains IN_PROGRESS; PE74 NOT_AUTHORIZED.

Exact accepted source identities:
- `tools/pe73_pi3_provision_environment.py`: SHA256 `a99f0fa72746ec3c455696627ec2ba6d53e4440dba0a483650d147d570aa8687`.
- `tests/test_pe73_pi3_provision_environment.py`: SHA256 `71a80ee01c85caf36a0712da4cbad3fb54551d2cba5015bcc12348b79f423eb7`.

Complete PI3 environment-only command (content identity remains fixed if main moves):

```sh
/usr/bin/python3 -I -B - <<'PY'
import hashlib,json,sys,urllib.request
url="https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/main/tools/pe73_pi3_provision_environment.py"
try:
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url,timeout=30) as response:
        if response.geturl()!=url:raise ValueError()
        raw=response.read(1048577)
    if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!="a99f0fa72746ec3c455696627ec2ba6d53e4440dba0a483650d147d570aa8687":raise ValueError()
except Exception:
    print(json.dumps({"RESULT":"BLOCKED_VERIFIED_PI3_ENVIRONMENT_SOURCE","STOP_REQUIRED":True}))
    raise SystemExit(1)
sys.argv=["pe73_pi3_provision_environment.py","prepare"]
exec(compile(raw,url,"exec"),{"__name__":"__main__","__file__":url})
PY
pe73_status=$?
printf 'PE73_PI3_ISOLATED_ENVIRONMENT_EXIT_STATUS=%s\n' "$pe73_status"
```

Pinned PI3 wheel identities:
- `cryptography-50.0.2-cp311-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl`: SHA256 `79def8d059362e7831389ed3be0ecdf58a89386e1271e35dd9f5af84e81bffd0`.
- `cryptography-50.0.2-cp311-abi3-musllinux_1_2_aarch64.whl`: SHA256 `25784ce8b9621c90c643efb9e1e2162ab3b0224cae446ad5e70e7fcb1ce18b51`.
- `pycparser-2.23-py3-none-any.whl`: SHA256 `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934`.
- `pip-25.3-py3-none-any.whl`: SHA256 `9655943313a94722b7774661c21049070f6bbb0a1516bf02f7c8d5d9201514cd`.
- `cffi-2.0.0-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.whl`: SHA256 `730cacb21e1bdff3ce90babf007d0a0917cc3e6492f336c2f0134101e0944f93`.
- `cffi-2.0.0-cp311-cp311-musllinux_1_2_aarch64.whl`: SHA256 `a05d0c237b3349096d3981b727493e22147f934b20f6f125a3eba8f994bec4a9`.
