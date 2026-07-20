# Phase 7A.8 Recovery Baseline

## Purpose

This file records the authoritative integrity and approval references for the completed Phase 7A.8 recovery validation chain.

## Governance

`docs/HIOC_MASTER_PLAN.md` remains authoritative. Phase 7A Passive Living Inventory remains active. Active Discovery remains postponed and disabled. This completed recovery milestone does not replace the Master Plan.

## Approved Recovery Epoch

`/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z`

## Approved Candidate

- Checkout: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/candidate/checkout`
- SHA: `be7b69d1da1a3b5c3c7a9e7ca27d1280b8f41cd1`
- Git tree: `12140b701d6f47ad51566a342a8d002aba6d78e0`
- Required state: detached and clean

## Approved Generation

`gen_1784229948679_0a45eaf2f2f7`

## Approved Archive Tool

- Path: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/recovery/archive_tool.py`
- SHA-256: `f6ac058527ab082cebce949921229c71b2c0c356b713f6d6961b2468af5fb57d`

## Recovery Validation Chain

| Checkpoint | Status | Evidence path | Archive path | Verified archive SHA-256 | Formal decision |
|---|---|---|---|---|---|
| R1 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/evidence` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/recovery-r1-evidence.tar.gz` | `53993481f55409948213276ce51b5cbb4311f65c040893c2314afef870028842` | PASS |
| Post-R1 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/recovery` | `Not independently verified during finalization` | `Not independently verified during finalization` | PASS |
| R2 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/evidence` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/recovery-r2-evidence.tar.gz` | `a746274587dd8ab3472b9b9a68aa3f790454ae28c3d76d4807323c4bd1d9c60c` | PASS |
| Post-R2 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/recovery` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/post-r2-review-20260716T202006Z.tar.gz` | `b7f5d30c41a11bd62dfed7eebb98e5a4614377e86f0063a75c19c03cac56aec3` | PASS |
| R3 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/evidence/R3-20260716T211337Z` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/recovery-r3-evidence-20260716T211337Z.tar.gz` | `76663f5e284db4780fcb4a6bc14558f73f6e5ce007bc5b509a53d8d3fcbfbae6` | PASS |
| Post-R3 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/recovery/post-r3-review-20260717T002055Z` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/post-r3-review-20260717T002055Z.tar.gz` | `6a228b3c173f11fb59c4273872613edf8765b831ee00f26d288da8369496df27` | PASS |
| R4 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/evidence/R4-20260717T005234Z` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/recovery-r4-evidence-20260717T005234Z.tar.gz` | `00eb21f43fa38f7737478afc4342266609a8718f130f57de63ae2d4d7d06be56` | PASS |
| Post-R4 | PASS | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/recovery/post-r4-review-20260717T013712Z` | `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/post-r4-review-20260717T013712Z.tar.gz` | `e607de6e1a8b04aa40cda42ccac92c3565ceeaad299ba02a0e390e90c76280ca` | A. R4 APPROVED |

## Final Approval

- R4 result: PASS
- Post-R4 decision: A. R4 APPROVED
- Validated commands: `validate`, `audit-status`, `list-generations`
- Generation delta: 0
- Receipt delta: 0
- Exact state equality: PASS
- Lifecycle lock: not acquired
- Scheduler lock: not acquired
- Production state access: none
- Inventory engine execution: none
- MQTT contact: none
- Active Discovery: off

## Baseline Protection

The recovery epoch, R1 through R4 evidence, Post-R1 through Post-R4 review evidence, migrated baseline, candidate checkout, and evidence archives are immutable historical evidence. Future work must create new timestamped evidence instead of altering them.

## Future Boundary

Recovery Baseline Finalization closes the completed recovery milestone. R5 may be planned only after this finalization is approved. R5 was not prepared or executed during this checkpoint. B4.2 was not executed. B4.3 was not prepared.

## Finalization Evidence

- Evidence directory: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/recovery/recovery-baseline-finalization-20260717T025244Z`
- Archive path: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z/archives/recovery-baseline-finalization-20260717T025244Z.tar.gz`
- `archive_identity_status = externally recorded`
- Finalization result: PASS
- Operator gate: Review documentation diff and evidence before commit; stop before R5

The archive SHA-256 and archive size intentionally are not embedded in archived artifacts or repository documentation. They are recorded externally in the operator's execution log to prevent cryptographic self-reference.
