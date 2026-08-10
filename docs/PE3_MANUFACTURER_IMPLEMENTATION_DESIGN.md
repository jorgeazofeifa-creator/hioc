# PE-3.1 Manufacturer Enrichment Implementation Design

Status: **COMPLETE — EXECUTABLE CONTRACT FROZEN; IMPLEMENTATION NOT STARTED**

## Purpose

This document records the implementation-design boundary. The complete normative
API, CLI, schema, transaction, failure, path, test, validation, and rollback
contract is [PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md](PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md).
That contract supersedes the earlier incomplete details and resolves the former
list-versus-map sidecar conflict. No executable or dataset was created by this
documentation correction.

## Frozen architecture

PE-3.1 is private descriptive Enrichment. It cannot select or modify identity,
canonical IP, inventory membership, PE-1 hostname evidence, PE-2 Assets, health,
liveness, incidents, topology, dependencies, service ownership, MQTT, Home
Assistant, dashboards, or notifications.

The execution model is a separate manually invoked local generator. It reads the
completed inventory artifact and an operator-built offline normalized database.
It writes separate private manufacturer sidecars. It has no inventory hook,
scheduler, service, daemon, timer, network lookup, automatic update, or download.

## Dataset governance

Local acquisition and local transformation are the only approved operating
model. The repository and releases may contain code, schemas, validators,
synthetic fixtures, and sanitized documentation. They must not contain IEEE
source files, copied registry rows, normalized IEEE-derived databases, or release
redistribution of registry content.

The future builder requires all three operator-supplied MA-L, MA-M, and MA-S
files and their checksums. It creates an immutable local version directory
containing a closed normalized database and adjacent manifest. Runtime parses
only that normalized artifact. Production acquisition, build, deployment, and
validation remain pending.

## Frozen storage and lookup

The database uses a closed ordered mapping keyed by prefix length and uppercase
hexadecimal prefix. Runtime creates immutable MA-L, MA-M, and MA-S maps and checks
36, 28, then 24 bits for EUI-48. Multicast and locally administered/randomized
addresses never produce a manufacturer claim. EUI-64 is validated and classified
but does not produce a manufacturer claim in PE-3.1; `FF:FE` is never removed.

`manufacturer.json` uses a closed mapping keyed by stable device ID. Every valid
inventory stable ID receives one record, including missing, invalid, excluded,
and unknown address results. `manufacturer_status.json` describes only the
manufacturer subsystem. Raw MACs, IPs, hostnames, and Asset values are prohibited.

## Failure and release boundary

Dataset, manifest, inventory-input, checksum, schema, lock, or write failure is
isolated from inventory and public systems. The last valid manufacturer sidecar
is preserved. A sanitized failure status is attempted independently. Immutable
database version directories and atomic directory promotion prevent mixed
database/manifest pairs.

Install, upgrade, and rollback deploy only implementation files and preserve
local manufacturer data, configuration, and private sidecars. They never bundle,
initialize, download, update, replace, or delete a dataset.

The dedicated manufacturer lock covers the complete generator transaction.
Only CLI, configuration, path resolution, and non-content preconditions precede
lock acquisition; mutable manufacturer inputs and the completed inventory
snapshot are opened and validated under the lock. This closes the validation-to-
generation time-of-check/time-of-use gap and serializes manufacturer generators
without acquiring the inventory, PE-1 enrichment, Asset, or another HIOC state
lock. The lock does not prevent external replacement of `inventory.json`; the
generator completes from the validated in-memory snapshot it loaded under its
own lock. The executable contract contains the sole normative transaction order.

## Validation and next gate

The exact future file set and minimum 92-test mapping are frozen in the executable
contract. Future production validation uses synthetic lookup proof plus sanitized
structural and aggregate verification for the locally generated real database;
no registry rows or manufacturer names enter repository evidence.

The next authoritative checkpoint is **PE-3.1 executable implementation** after
explicit authorization. PE-3 production deployment and PE-4 are not started.
