# Production Incident: DHCP Pool Exhaustion, 2026-07-29

## Status

Resolved. Production validation passed after the DHCP pool was expanded and critical network settings were validated.

## Root Cause

The immediate production outage was caused by exhaustion of the configured DHCP dynamic address pool. The previous pool, `192.168.100.50 - 192.168.100.150`, had no usable capacity for a client that needed an address. The DHCP daemon could remain active while DHCP service delivery was degraded: process health showed that the daemon ran, but capacity exhaustion prevented at least one client from obtaining a usable lease.

This evidence does not establish that every connectivity symptom observed that day had the same cause. It establishes the cause of the confirmed address-allocation failure.

## Timeline

- **2026-07-29:** Connectivity symptoms were investigated.
- The DHCP dynamic pool was identified as exhausted.
- The pool was expanded from `192.168.100.50 - 192.168.100.150` to `192.168.100.50 - 192.168.100.250`.
- A previously failing Android device immediately obtained a valid lease.
- PI3 NUT&PIHOLE and PI5 Home Assistant static networking were validated.
- DHCP, DNS resolution, Internet connectivity, Pi-hole FTL, NUT, Home Assistant Supervisor, router reachability, and Pi-hole reachability were validated.
- HIOC deployment validation completed with result **PASS**.

Exact event times were not recorded in the supplied production evidence.

## Evidence

| Evidence | Validated value |
| --- | --- |
| Previous DHCP pool | `192.168.100.50 - 192.168.100.150` |
| Current DHCP pool | `192.168.100.50 - 192.168.100.250` |
| Post-change usage | 138 active leases, 63 free addresses, 68.7% utilization |
| Gateway | `192.168.100.1` |
| PI5 Home Assistant | `192.168.100.251`, DNS `192.168.100.252`, gateway `192.168.100.1` |
| PI3 NUT&PIHOLE | `192.168.100.252` |
| Client recovery | Previously failing Android device obtained a lease immediately after expansion |
| HIOC validation | `HIOC Deployment Validation: PASS` |

The lease counts and utilization are point-in-time evidence from July 29, 2026, not permanent state or a live metric.

## Resolution

- Expanded the dynamic DHCP pool to `192.168.100.50 - 192.168.100.250`.
- Preserved PI3 NUT&PIHOLE at static address `192.168.100.252`.
- Moved PI5 Home Assistant from DHCP to static address `192.168.100.251`.
- Configured and validated PI5 DNS as `192.168.100.252` and gateway as `192.168.100.1`.
- Completed the infrastructure and HIOC production validation checks listed above.

DHCP capacity monitoring was not implemented during the response. It is planned in the Master Plan's future DHCP Service Health & Capacity Monitoring phase.

## Validation

Production checks passed for PI3 static networking, PI5 static networking, DHCP operation, DNS resolution, Internet connectivity, Pi-hole FTL, NUT, Home Assistant Supervisor, router reachability, Pi-hole reachability, and HIOC deployment. See [NETWORK_FOUNDATION.md](NETWORK_FOUNDATION.md) for the current network contract and [OPERATIONS.md](OPERATIONS.md) for the HIOC runtime-health model.

## Lessons Learned

- A healthy daemon does not guarantee healthy service delivery.
- Capacity is part of service health.
- Critical infrastructure must be documented as first-class assets and dependencies.
- Runtime operation must be documented explicitly rather than rediscovered through SSH.
- Historical failures remain useful evidence after resolution.
- Cron-driven systems require freshness-based validation rather than persistent-process checks.

The [System Reference Manual](SYSTEM_REFERENCE.md) records the current system, while [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md) governs future work.
