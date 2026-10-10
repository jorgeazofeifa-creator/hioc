# PE-4 Public Projection historical/current lifecycle test-binding correction

Correction status: PASS/CLOSED. Production deployment: NOT APPLICABLE / NO DEPLOYMENT.
Public Projection closure: NOT CLOSED. PE-4: NOT COMPLETE. Phase 7A: ACTIVE.
PE-5: NOT STARTED. Production evidence remains OPERATOR_SUPPLIED and was not rerun.

## Defect and intended behavior

Historical checkpoint tests read the evolving current Master Plan while several
current test source bytes were simultaneously required to equal original
historical source bytes. This prevented legitimate subsequent lifecycle transitions.
Historical source identity and current lifecycle test identity are now distinct.
Original records, schemas, commits, blobs, hashes and historical_only flags remain
immutable. Exactly four named tests receive the successor current-byte identity
contract. There are no runtime, document, tool, release, schema or directory exceptions.

## Exact historical snapshot selection

- tests/test_pe4_ha_association_scheduler_deployment_closure.py: eda070d4b06ccd7f562a74e1cb6b42cb5c630d67. The Public Projection preparation commit introduced the scheduler test assertions for the public projection preparation lifecycle and PI3 source synchronization.
- tests/test_pe4_ha_association_implementation_preparation.py: c762745b428b28518cf4415f7399ff2cacb70c66. The Public Projection implementation commit introduced this test revision and its Public Projection implementation-era roadmap and next-task assertions.
- tests/test_pe4_ha_runtime_credential_provisioning.py: c762745b428b28518cf4415f7399ff2cacb70c66. The Public Projection implementation commit introduced this test revision and its Public Projection implementation-era roadmap and next-task assertions.
- tests/test_pe4_ha_runtime_credential_provisioning_closure.py: c762745b428b28518cf4415f7399ff2cacb70c66. The Public Projection implementation commit introduced this test revision and its Public Projection implementation-era roadmap and next-task assertions.


## Enforcement

Both implementation and POSIX source-binding tests always verify the original
source commit, bytes, SHA-256 and Git blob. Historical-only sources retain their
original semantics. Every other nonhistorical source must match current normalized
bytes exactly. For the four exceptions, the closed successor record verifies
the original identity, exact test classification and current SHA-256/Git blob.
Current artifact bindings separately govern changed test and Master Plan artifacts;
they grant no source-equality exception to runtime or document paths.

The focused suite rejects unknown/fifth paths, docs/runtime/tool/release/schema/
governance paths, missing source entries, historical/current hash or blob changes,
authority/flag changes, runtime or production changes, lost provenance, wildcard/
directory paths, missing/current lifecycle authority, and unsupported lifecycle claims.
It also proves that unexplained changed nonexception runtime bytes still fail.

## Review of the ten closure-draft test changes

- tests/test_pe4_ha_association_implementation_preparation.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. The Public Projection implementation commit introduced this test revision and its Public Projection implementation-era roadmap and next-task assertions.
- tests/test_pe4_ha_association_independent_production_acceptance_closure.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. Only historical observation scope changes. The explicit c7db snapshot owns the existing preparation/acceptance/baseline-era assertions.
- tests/test_pe4_ha_association_public_projection.py: B. PUBLIC_PROJECTION_CLOSURE_ONLY. The draft closure-artifact overlay is preserved unstaged; staged source enforcement uses this correction authority only.
- tests/test_pe4_ha_association_public_projection_deployment_baseline_correction.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. Only historical observation scope changes. The explicit c7db snapshot owns the existing preparation/acceptance/baseline-era assertions.
- tests/test_pe4_ha_association_public_projection_deployment_preparation.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. Only historical observation scope changes. The explicit c7db snapshot owns the existing preparation/acceptance/baseline-era assertions.
- tests/test_pe4_ha_association_public_projection_posix_source_validation_closure.py: C. MIXED_CORRECTION_AND_CLOSURE. The draft closure-artifact overlay is preserved unstaged; staged source enforcement uses this correction authority only.
- tests/test_pe4_ha_association_public_projection_preparation.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. Only historical observation scope changes. The explicit c7db snapshot owns the existing preparation/acceptance/baseline-era assertions.
- tests/test_pe4_ha_association_scheduler_deployment_closure.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. The Public Projection preparation commit introduced the scheduler test assertions for the public projection preparation lifecycle and PI3 source synchronization.
- tests/test_pe4_ha_runtime_credential_provisioning.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. The Public Projection implementation commit introduced this test revision and its Public Projection implementation-era roadmap and next-task assertions.
- tests/test_pe4_ha_runtime_credential_provisioning_closure.py: A. HISTORICAL_CURRENT_LIFECYCLE_BINDING_CORRECTION. The Public Projection implementation commit introduced this test revision and its Public Projection implementation-era roadmap and next-task assertions.


## Evidence report

Deployment Result: NOT APPLICABLE / NO DEPLOYMENT.
Intended Behavior: separate immutable historical checkpoint provenance from
evolving lifecycle assertions without weakening source protection.
Invariant Checks: historical records/hashes/blobs/flags unchanged; exact four
exceptions; nonexception runtime bindings strict; no wildcard; no production
activity; No-Assumptions law preserved.
Warnings: Public Projection production closure remains pending; closure draft
preserved in a named keep-index stash and an exact-byte workstation manifest;
production evidence not rerun.
Result: validation and commit are permitted only after all required suites pass.
No production state is inferred from this repository correction.
