# PE-4 Home Assistant Access and Privacy Contract

**Status:** Active PE-4.0A contract

**Scope:** Repository governance before live discovery

**Next gate:** PE-4.0B.2a preparation, separately authorized

## Purpose and status

This document is the authoritative pre-discovery contract for PE-4 Home
Assistant Association. PE-4.0A and the credential-free PE-4.0B.1 production
preflight are complete. PE-4.0B.2 authenticated discovery and PE-4
implementation are not started. This contract does not authorize PI5 access,
credentials, discovery, deployment, or mutation.

## PE-4.0B.1 accepted preflight and next boundary

The accepted preflight classified PI5 as an `HA_TERMINAL_ADDON` with
interactive zsh on HA OS 18.1, Core 2026.8.1, and supported/healthy Supervisor
2026.07.5. The governed endpoint is exactly `http://192.168.100.251:8123`, with
no proxy influence and TLS not applicable. Python 3.14.5 and the other reviewed
client tools are available, a secure prompt is available, and no dedicated
WebSocket client was detected. That absence is not itself a blocker and does
not prove that any Python WebSocket module is installed.

PE-4.0B.2 is subdivided into separately authorized STOP boundaries:

1. **PE-4.0B.2a — authenticated API/capability proof.** A standalone,
   repository-controlled Python process must obtain the operator-controlled
   credential with `getpass` from the controlling terminal, retain it only in
   process memory, prove authentication and the supported read-only capability,
   and stop. Exact registry commands must not be guessed.
2. **PE-4.0B.2b — registry/schema discovery.** Only a separately reviewed 2a
   PASS may permit preparation of bounded structural discovery. It must not run
   automatically after 2a.

Preparation must decide between a proved already-installed Python WebSocket
library and a technically reviewed repository-controlled standard-library
client. It must install no package and must fail closed if neither mechanism is
proved safe. REST alone is not assumed sufficient for registry metadata.

Future evidence is invocation-owned under
`/tmp/hioc-pe4-ha-discovery-XXXXXXXX`: directory mode `0700`, sanitized files
mode `0600`, `discovery-report.json`, and result-last
`discovery-result.txt`. Raw responses stay memory-only; there is no raw or
redacted-raw dump and no caller-selected evidence path.

PE-4 adds Home Assistant association evidence to an already-reconciled HIOC
identity. It is not a new identity engine and cannot change stable HIOC IDs,
MAC identity, canonical IP, liveness, health, incidents, expected availability,
or operator-owned Asset fields.

## Repository-known facts and live-discovery inputs

Repository-known facts are limited to the current consumer-side MQTT packages,
templates, dashboards, and the PE-4 authority/privacy requirements below. No
repository ingestion path from a Home Assistant device, entity, area, or config
entry registry exists. Deployment type, supported endpoint, API capabilities,
credential type, safe credential injection method, TLS trust, and registry
schema require a separately prepared and authorized PE-4.0B inspection on PI5.
They must not be guessed.

## Access-authority matrix

| Source class | Classification | Contract |
|---|---|---|
| Authenticated supported REST API | SUPPORTED CANDIDATE | Eligible only after PE-4.0B proves the deployed version exposes the minimum registry structure read only, without collecting states or invoking services. |
| Authenticated supported WebSocket API | SUPPORTED CANDIDATE | Preferred over internals when it provides equivalent supported registry reads; exact commands and authentication remain unfrozen pending live classification. |
| `.storage` device/entity/area/config-entry files | PROHIBITED | Internal implementation files are not an approved compatibility interface. No direct read or write, recursive scan, or fallback is authorized. |
| Recorder, SQLite, or external HA database | PROHIBITED | PE-4 needs registry association structure, not history or live state. Direct database access or mutation is forbidden. |
| Existing MQTT data | INSUFFICIENT INFORMATION | Repository MQTT is a HIOC-to-HA publication path, not proven HA registry evidence and not identity authority. |
| Existing HIOC-facing HA packages | DISCOVERY ONLY | They establish current consumer integration context but contain no approved registry acquisition interface. |
| Add-on, supervisor, shell, or container filesystem access | PROHIBITED | Deployment convenience cannot bypass the supported-interface and read-only requirements. |

If no supported read-only interface is proved, PE-4.0B stops with
`UNSUPPORTED_INTERFACE`; it must not fall back to internals.

## Identity and trust authority

| Evidence | Authority |
|---|---|
| Exact normalized HA device MAC connection matching exactly one existing MAC-backed HIOC identity | STRONG CANDIDATE, subject to PE-4.0C schema freeze |
| Integration-specific identifier, canonical IP corroborating a MAC match, hostname, manufacturer, model, config-entry ownership, device name, or HA area | SUPPORTING ONLY |
| IP-only, hostname-only, name similarity, area match, or manufacturer/model similarity | WEAK / REVIEWABLE ONLY |
| Friendly name, entity ID, area, manufacturer/model, availability/state, helper/template/group/scene/automation, entity without physical device identity, or conflicting MAC evidence | REJECT AS INDEPENDENT IDENTITY |

HIOC remains authoritative for stable device ID, MAC identity, and canonical IP.
Home Assistant is authoritative only for its own registry metadata: registry
device identity, entity membership, integration ownership, area candidate, and
registry naming metadata. Operator-managed Asset knowledge remains the highest
authority for descriptive fields. HA evidence cannot overwrite an Asset field.

## Permitted read categories

PE-4.0B may read only the minimum information needed to derive sanitized schema
and relationship evidence:

- HA version, safely observable deployment/interface classification, and an
  approved non-sensitive instance reference;
- device/entity/area/config-entry field names, types, optionality, namespaces,
  relationship presence, and aggregate cardinalities;
- aggregate device, entity, area, and config-entry counts;
- aggregate entity-with-device, entity-without-device, disabled, via-device,
  physical-device-backed, helper, template, group, scene, automation,
  integration-level, and virtual/cloud classification counts;
- aggregate zero/one/multiple connection and MAC-connection counts, connection
  type namespaces, identifier namespace names, and collision/conflict counts.

These reads characterize schema and association authority; they are not a
household inventory export. Unsupported or unknown fields are counted and
reported by category, never returned as raw records.

## Prohibited reads, exposure, and mutation

Discovery must not collect or publish raw entity states or historical states,
automation contents, configuration values, secrets, tokens, credentials,
location/GPS data, Wi-Fi data, webhook IDs, API keys, or secret-bearing URLs.
It must not return or retain raw MAC or IP addresses, hostnames, entity IDs,
unique IDs, device/area/room/person/user names, registry IDs, integration-
specific identifiers, or other household metadata.

Home Assistant service calls, state writes, registry writes, config-entry or
integration reload, token creation/deletion, add-on changes, database mutation,
`.storage` mutation, YAML changes, restart/reboot, automation execution, MQTT
publication, HIOC inventory/Asset/manufacturer/incident mutation, systemd
mutation, and cron mutation are prohibited. A source that cannot satisfy this
read-only contract is ineligible.

## Credentials and network transport

Credentials are operator-controlled, never committed, echoed, logged, printed,
embedded in evidence or documentation, or persisted by discovery tooling.
Their scope must be read-only to the greatest extent supported; administrator
mutation privileges cannot be required merely for convenience. The repository
cannot yet safely freeze the exact credential type or token-generation flow.
PE-4.0B preparation must determine the deployed supported mechanism and a
non-echoing, non-command-line safe invocation method. Failure to do so stops.

PE-4.0B preparation must freeze the exact allowlisted endpoint, localhost or
network route, HTTP/HTTPS policy, certificate trust, redirect and proxy policy,
DNS use, connect/read/total timeouts, and retry limit. Secret-bearing URLs and
silent redirects outside the allowlist are prohibited. TLS verification must
not be disabled to make access work; local/self-signed trust requires an
explicit operator-approved trust input.

## Privacy and MAC boundary

Raw registry material is private household data. Count-only evidence is the
default. Categorical values and boolean presence are allowed when counts cannot
express the schema. A deterministic one-way hash is allowed only when PE-4.0B
proves it is necessary, scoped to the invocation or approved instance
provenance, and not an avoidable persistent household fingerprint.

Schema discovery may confirm that MAC connection entries exist and determine
their type, encoding class, normalization needs, multiplicity, and aggregate
collision behavior without printing a MAC. Later governed association code may
process raw MACs locally under the frozen PE-4.0C contract, but raw MACs do not
enter discovery evidence, Git, logs, MQTT, or operator output.

Live entity state and availability are discarded before evidence processing if
a supported response unavoidably contains them. They have no PE-4 identity,
liveness, health, incident, or expected-availability authority.

## Instance provenance

Evidence requires a deterministic, non-secret, non-personally-identifying
reference that distinguishes multiple HA instances and is stable enough to
attribute later observations. PE-4.0B must choose between an operator-configured
logical reference, an approved supported HA UUID, or a sanitized fingerprint
after live interface classification. Raw instance names, URLs, hostnames, and
unapproved identifiers are not evidence fields.

## Bounded invocation and raw-data lifecycle

PE-4.0B is one bounded invocation: explicit maximum response bytes and record
count, connect/read/total timeouts, a finite retry limit (preferably none), no
polling loop, recurring discovery, historical retrieval, recursive filesystem
scan, or continuous monitoring. Exceeding a bound fails closed.

Raw responses remain in memory where possible. If temporary storage is
unavoidable, it belongs only to an invocation-owned private directory, has
operator ownership and restrictive mode, rejects symlinks, and is removed
before sanitized result publication. If cleanup cannot be proved, publication
fails closed. Raw data never enters Git or long-term association storage.

## Sanitized evidence contract

Future evidence may contain only: report schema version; result; target and HA
deployment/interface classifications; HA version; approved instance reference;
structure fingerprint; top-level key/type inventory; aggregate registry and
relationship counts listed above; connection and identifier namespace names;
zero/one/multiple connection and MAC counts; collision/conflict, via-device,
unknown-field, and virtual-entity counts; privacy result; bounded warnings;
`ERROR_CODE`; and `FAILURE_STAGE`. It contains no raw registry record.

Evidence is written to a tool-created invocation-owned private directory with
operator ownership, restrictive permissions, no symlink traversal, no caller-
supplied arbitrary path, atomic files where appropriate, and directory/file
durability before result-last publication. The sanitized result is published
last. PASS evidence is preserved unchanged for PE-4.0C review. Failure evidence
may be retained only if it passes the same privacy validation. Retention of
future associations is a separate contract.

## Failure and STOP contract

Bounded error codes are `WRONG_TARGET`, `WRONG_OPERATOR`,
`UNSUPPORTED_HA_DEPLOYMENT`, `UNSUPPORTED_INTERFACE`,
`AUTHENTICATION_UNAVAILABLE`, `AUTHENTICATION_FAILED`,
`INSUFFICIENT_READ_SCOPE`, `UNEXPECTED_SCHEMA`,
`PRIVACY_CONTRACT_VIOLATION`, `DISCOVERY_OUTPUT_UNSAFE`,
`EVIDENCE_PUBLICATION_FAILED`, and `UNEXPECTED_ERROR`.

Bounded stages are `TARGET_IDENTITY`, `HA_DEPLOYMENT_DISCOVERY`,
`AUTHENTICATION`, `INTERFACE_DISCOVERY`, `SCHEMA_DISCOVERY`,
`PRIVACY_VALIDATION`, and `EVIDENCE_PUBLICATION`. Every failure emits a bounded
sanitized result when safe, stops, and performs no fallback mutation or
automatic rollback. Unsupported interfaces, unexpected schemas, unsafe output,
uncertain cleanup, and zero or ambiguous authority evidence fail closed.

## PE-4.0B preparation gate

PE-4.0B preparation must determine the PI5/HA deployment type, approved
supported endpoint and registry-read semantics, credential availability and
safe injection, TLS/network inputs, exact query/response bounds, sanitized
evidence schema, and one read-only operator procedure. It must prove that these
requirements can be met before any live access. PE-4.0B and PE-4 implementation
remain not started until separately authorized.
