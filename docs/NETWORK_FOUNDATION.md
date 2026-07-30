# HIOC Network Foundation

## Authority and Evidence

This document owns the current documented network foundation on which HIOC depends. Values labeled production evidence were operator-validated on July 29, 2026. This is not a complete reservation inventory or live monitoring view.

## Confirmed Foundation

| Subject | Confirmed role and configuration |
| --- | --- |
| Router and gateway | `192.168.100.1`; provides the confirmed gateway and routed network access. Model-specific configuration is not documented. |
| PI3 NUT&PIHOLE | Static `192.168.100.252`; hosts Pi-hole, DHCP, DNS, Unbound, NUT, and HIOC scheduled engines. |
| Pi-hole | DNS and DHCP service on PI3. |
| DHCP | Dynamic pool `192.168.100.50 - 192.168.100.250`. The former `.50 - .150` pool is historical incident context. |
| DNS | PI5 uses `192.168.100.252` as DNS. Pi-hole uses locally observed Unbound for recursive resolution. Detailed production configuration paths require production verification. |
| Unbound | Present on PI3 and observed listening locally at `127.0.0.1:5335`. |
| PI5 Home Assistant | Static `192.168.100.251`, DNS `192.168.100.252`, gateway `192.168.100.1`. |
| NUT | Hosted on PI3. UPS device details are not yet documented. |
| MQTT | HIOC reads and publishes MQTT through repository-defined clients and toolkit configuration. Broker host, authentication, and production port are secret or environment-managed and are not recorded here. |

On July 29, 2026 the pool had 138 active leases, 63 free addresses, and 68.7% utilization. These are dated point-in-time evidence, not current live values. See [INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md](INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md).

## Static Address Policy

- Critical infrastructure uses documented stable addresses outside the dynamic DHCP pool.
- Every static address must record owner, purpose, dependency role, and validation method.
- DHCP pool changes must be checked against every documented static assignment.
- Address-allocation changes must update this document and [SYSTEM_REFERENCE.md](SYSTEM_REFERENCE.md).

Confirmed assignments:

| Address | Owner | Purpose | Validation |
| --- | --- | --- | --- |
| `192.168.100.251` | PI5 Home Assistant | Home Assistant host | Static networking, DNS, gateway, Supervisor, router and Pi-hole reachability validated 2026-07-29 |
| `192.168.100.252` | PI3 NUT&PIHOLE | DNS, DHCP, Pi-hole, Unbound, NUT, HIOC | Static networking and hosted infrastructure validated 2026-07-29 |

## MQTT Data Flow

Repository-supported HIOC publishers include the history engine, Incident Engine v2, inventory engine, platform-status publisher, and read-only runtime validator. The separately deployed PI4 MQTT Health Publisher publishes toolkit health data; its implementation is outside this repository and detailed outputs require production verification. Topic contracts are documented in [MQTT.md](MQTT.md).

## Critical Dependencies

| Consumer | Dependency | Status |
| --- | --- | --- |
| Network clients | DHCP for dynamic address allocation | Confirmed |
| Network clients | `192.168.100.1` for routed access | Confirmed |
| PI5 Home Assistant | PI3 `192.168.100.252` for DNS | Confirmed |
| Pi-hole | Local Unbound at `127.0.0.1:5335` for the observed recursive-resolution path | Confirmed by production observation; detailed configuration requires verification |
| HIOC runtime | PI3 availability, cron, deployed files, persistent state, and configured data sources | Confirmed |
| Home Assistant integrations | PI3-hosted MQTT, NUT, and HIOC-generated data where configured | Repository-derived; exact production integration inventory requires verification |

These are current operational dependencies, not a completed implementation of the future topology or digital-twin roadmap.
