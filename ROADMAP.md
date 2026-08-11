# HIOC Roadmap

## Document Ownership

This file is the short public roadmap summary.

The detailed implementation roadmap is maintained in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md).

## Current Phase

Phase 7A - Passive Living Inventory.

Goal: enrich the Living Inventory using passive infrastructure data only.

## Authoritative Passive-Enrichment Sequence

The detailed status and sequencing authority is
[docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md). The agreed order is:

1. PE-1 - Hostname Enrichment — complete, production validated.
2. PE-2 - Asset Foundation — complete, production validated.
3. PE-3 - Manufacturer Reference Enrichment — PE-3.0 through PE-3.3 complete at
   their stated design/repository/external-validation gates; production
   deployment and PI3 validation remain pending.
4. PE-4 - Home Assistant Association — not started.
5. PE-5 - MQTT and Passive Service Association — not started.
6. PE-6 - Classification & Metadata Quality — not started.
7. PE-7 - Expected Availability & Permanent IoT Monitoring — planned.
8. PE-8 - Automation Correlation & Impact Analysis — planned.
9. PE-9 - Service & Infrastructure Dependency Intelligence — planned.

Retention/archival, DHCP service health/capacity, notification semantics,
incident-history validator hardening, infrastructure disaster recovery, and
hardware migration remain separate governed future checkpoints.

## Next Phase

Phase 7B - Safe Active Discovery.

Status: planned, not started.

Active discovery remains postponed until Phase 7A is complete.

## Future Phases

Future work is tracked in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md).
