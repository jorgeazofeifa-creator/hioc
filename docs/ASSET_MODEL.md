# HIOC Asset Model

## Purpose

HIOC currently discovers technical device identities and explains their observed state. The long-term direction is broader: evolve the Living Inventory into an asset-centric living digital twin of the home infrastructure.

An asset-centric system does not merely know that a MAC address exists. It can eventually connect that technical evidence to operator knowledge: what the equipment is, where it is, why it matters, who is responsible for it, when it should be available, and what action is appropriate when its state changes.

This document explains that direction. Planned concepts are not claims about current runtime behavior.

## Evidence Sources

Different sources answer different questions. HIOC must retain their provenance because no single source proves everything.

| Source | What it can prove | What it does not prove |
| --- | --- | --- |
| ARP or neighbor tables | A network identity was recently associated with an address on the local network. | That the device is still present, healthy, or expected to be available. Unresolved entries are not positive observations. |
| DHCP leases | A server assigned or retained an address for a client identity. | Current presence, reachability, correct operation, or ownership. A lease can outlive the client's connection. |
| Known infrastructure | An operator has supplied identity, role, naming, location, notes, or topology knowledge. | That the equipment is currently reachable or functioning. |
| Local collector | The collector can identify its own interfaces, addresses, operating system, and local services. | The state of unrelated network devices or every service dependency. |
| Integrations | An authoritative external system can contribute device, service, relationship, or status information within that integration's scope. | Facts outside the integration's authority. Integration quality and freshness still matter. |
| Future active discovery | Approved probes may confirm that an address or service responds at a point in time. | Business purpose, ownership, expected availability, or complete health. Active Discovery remains postponed until Phase 7B. |

Source authority matters. Operator metadata may name and classify an asset, while discovery evidence owns observations. A weak source must not overwrite a stronger identity or fabricate availability.

## Observation

An observation is positive evidence that HIOC saw a device through a source capable of demonstrating current presence. It records what was seen, when it was seen, and how it was seen.

An observation is not necessarily proof that the device is functioning correctly. A host may answer on the network while an important service is degraded. Conversely, a mobile device may not be observed because it legitimately left the home.

DHCP assignment is identity and address evidence, not liveness evidence. It does not create or refresh a positive-observation timestamp.

## Observation States

Current device records can expose these observation states:

- `recent`: usable positive evidence is within the current freshness window.
- `stale`: the last positive evidence is older than the stale threshold.
- `expired`: the last positive evidence is older than the offline threshold.
- `unobserved`: a configured identity is known, but positive discovery has not yet seen it.
- `unknown`: HIOC lacks usable positive-observation history from which to calculate freshness.

Stale does not automatically mean failed. Expired does not automatically mean failed. Unknown does not mean healthy, offline, or recently seen; it means usable history is unavailable.

## Operational Health

Observation freshness and operational health answer different questions:

- **Healthy** means current authoritative evidence supports normal operation.
- **Watch / Observation** means evidence is old, incomplete, or worth reviewing, but failure is not proven.
- **Degraded** means stronger evidence indicates a problem or reduced operation.
- **Offline** means HIOC has sufficient authority and an availability expectation to conclude that an asset expected to be available is unavailable.

The current monitoring policy deliberately avoids turning ordinary ARP/DHCP-only clients into incidents solely because their observations age. Future policy can become more asset-aware, but it must preserve the principle that observation is not availability.

## Device and Asset

A **Device** is a discovered technical identity. It may contain a stable device ID, MAC address, IP address, hostname, sources, services, observation history, and health or status fields.

An **Asset** is a Device linked to operator-provided meaning and expectations. An asset may eventually include a friendly name, physical location, purpose, owner, category, criticality, expected availability, monitoring and maintenance expectations, notes, an optional photo, purchase or installation dates, maintenance history, and retirement or archival state.

Examples show why the distinction matters:

- A family phone may legitimately leave the network every day. Its disappearance is useful history, not necessarily a failure.
- A smartwatch may be powered off or away from home without requiring action.
- A Pi-hole server is normally expected to remain available, so authoritative loss of service may require attention.
- A garage controller or leak sensor may be small, but its absence may matter because of its purpose and expected availability.
- An old guest device may remain historically useful and later become eligible for archival.

Asset knowledge should survive address changes and rediscovery because it is linked to stable identity rather than a temporary IP address.

## Planned Criticality and Availability Concepts

The following are planning examples, not finalized schema names or implemented policies.

Possible criticality classes include:

- **Critical**: loss can undermine safety or core infrastructure.
- **Important**: loss materially affects household operations.
- **Normal**: useful equipment with ordinary impact.
- **Transient**: mobile, guest, temporary, or intermittently present equipment.

Possible expected-availability patterns include:

- always available;
- usually available;
- scheduled;
- mobile or transient;
- informational only.

Every device cannot use one universal availability rule. Expected availability must be known before disappearance can reliably be treated as failure, and criticality helps determine urgency after a failure is established.

## Retention and Archival Safety

Retention remains a planned policy checkpoint. Stale age alone must never cause an important asset to be forgotten.

Future retention and archival decisions must consider asset classification, operator ownership, criticality, expected availability, monitoring expectations, observation history, authoritative sources, and explicit operator decisions.

The safety principles are:

- Important or explicitly monitored assets must not be silently archived merely because they disappeared.
- Transient, guest, or retired assets may be eligible for configurable archival.
- Archival is not permanent deletion.
- Archived assets should remain searchable and be able to reappear under the same stable identity.
- Permanent deletion must be governed by explicit operator confirmation or an approved policy.
- Historical identity and incident evidence should be preserved according to policy.

Asset classification is therefore a prerequisite for aggressive archival. Until that policy is designed and approved, current retention behavior remains unchanged.

## Long-Term Vision

Build a living digital twin of the home infrastructure that continuously discovers, identifies, understands, monitors, and explains the operational state of every meaningful asset, surfacing only conditions that require human attention.

Current HIOC capabilities provide stable technical identities, passive evidence, services, relationships, observation state, health presentation, and operator-supplied known-infrastructure enrichment. The richer asset model, lifecycle workflows, expected-availability policies, maintenance history, and predictive asset intelligence are planned evolution—not completed behavior.
