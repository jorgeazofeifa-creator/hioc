# PE-4 Home Assistant Access and Privacy Contract

**Status:** Active PE-4.0A contract

**Scope:** Repository governance before live discovery

**Next gate:** PE-4.0B.2a client commit review, separately authorized

## Repository-controlled 2a client

The client corrects the **PE-4.0B.2A WEBSOCKETS REDIRECT-SUPPRESSION
ENFORCEMENT DEFECT — CLIENT ACCEPTS A DEPENDENCY API THAT MAY FOLLOW HANDSHAKE
REDIRECTS WITHOUT AN EXPLICIT ZERO-REDIRECT CONTROL** by creating one bounded
TCP connection to the exact governed target and supplying that pre-existing
socket to `websockets.connect()`. The supported dependency rejects every
handshake redirect when a pre-existing socket is supplied, so no alternate URI
can be contacted and no token-bearing frame can reach a redirected endpoint.
The dependency/API gate runs before `getpass`; future runtime preparation must
emit `REDIRECT_SUPPRESSION_CAPABILITY=PASS` or fail with
`REDIRECT_SUPPRESSION_UNAVAILABLE/WEBSOCKET_API_COMPATIBILITY`.

`tools/hioc-pe4-ha-auth-capability.py` now implements this frozen contract in
repository source. It requires the exact non-secret target tuple through
`--expected-hostname a0d7b954-ssh --expected-operator root --target-ipv4
192.168.100.251 --target-port 8123 --instance-label PI5_HA`; it accepts no URL,
secret, evidence path, or command argument. It proves an approved installed
Python WebSocket dependency before target-gated terminal credential acquisition.
After correction of the post-materialization websocket-client bound defect, the
only approved path is `websockets` with explicit `max_size=65536`, proxy
suppression, and connect/close timeout parameters. It installs nothing.
The superseded path is classified as **PE-4.0B.2A WEBSOCKET-CLIENT
MESSAGE-BOUND ENFORCEMENT DEFECT — PREFERRED DEPENDENCY PATH APPLIES THE
65,536-BYTE LIMIT ONLY AFTER UNBOUNDED MESSAGE MATERIALIZATION**.

The source has offline fake-based tests but has not been deployed or executed
against PI5 or live Home Assistant. Its Git blob and worktree SHA-256 are to be
frozen at review. A separate checkpoint must decide whether governed source
execution or a runtime deployment is appropriate and must prove the selected
dependency identity before preparing any operator command. PE-4.0B.2a therefore
remains **NOT STARTED**; implementation presence is not production PASS.

## Frozen PE-4.0B.2a official API contract

The current, versionless Home Assistant developer documentation applies to the
deployed Core 2026.8.1 contract; registry-source conclusions below are pinned
separately to the official `2026.8.1` Core tag.

The 2a sequence is `REST_THEN_WEBSOCKET_2A`:

1. Send one authenticated `GET` to the exact trailing-slash path `/api/` at
   `http://192.168.100.251:8123`, with `Authorization: Bearer <access-token>`
   assembled only in process memory. Require HTTP 200, JSON content, and the
   exact closed object `{"message":"API running."}`; discard the body.
2. Connect without redirects or proxy use to
   `ws://192.168.100.251:8123/api/websocket`. Require an `auth_required` object,
   send exactly `{"type":"auth","access_token":<access-token>}`, and require
   `auth_ok`. `auth_invalid` is `AUTHENTICATION_FAILED` and the connection is
   closed. Send no command and close after authentication.

REST 401 means `AUTHENTICATION_FAILED`; documented REST statuses also include
400, 404, and 405, which are unexpected for the frozen root request. WebSocket
command messages, if ever authorized later, carry a unique integer `id` and
receive a `result` object with the same `id`, `success`, and either result or
error information. Event subscriptions require an explicit command and are
prohibited. There is **NO_GENERAL_CAPABILITY_DISCOVERY_DOCUMENTED**:
`supported_features` enables client features and is not a server command list.

The documented REST API provides no device-, entity-, area-registry, or
config-entry relationship listing: all four are
`NOT_SUPPORTED_BY_DOCUMENTED_REST`. Core 2026.8.1 source registers
`config/device_registry/list`, `config/entity_registry/list`,
`config/area_registry/list`, and `config_entries/get` as WebSocket commands
without `require_admin`; source therefore classifies their read permission as
`AUTHENTICATED_USER_SUFFICIENT`. They expose raw household records and belong
only to 2b. Except for the separately documented
`config/entity_registry/list_for_display`, these config/frontend commands are
not presented as a stable public registry API in the developer WebSocket
documentation. Source existence must not be silently elevated into an external
compatibility promise; 2b requires a separate version-pinned review.

The operator supplies an HA access/bearer token through Python `getpass`.
There is no argv, environment, shell variable, file, log, evidence, printed
header/frame, alternate secret source, or token-generation workflow. The token
exists only in process memory and references are released promptly without
claiming Python zeroization. `INSTANCE_REFERENCE_METHOD=OPERATOR_LOGICAL_LABEL`
and the label is `PI5_HA`; all HA instance names, URLs, locations, UUIDs,
installation IDs, and user IDs are discarded.

2a is terminal-only and creates no evidence directory. Its limits are connect
5 seconds, read 10 seconds, total network budget 20 seconds, 65,536 bytes per
response, two credential-bearing requests, zero retries, zero redirects, no
polling, subscriptions, background work, registry enumeration, or state
enumeration. A credential-free precheck must prove that `websockets` is
importable and exposes the required `max_size`, proxy, and timeout parameters;
module importability alone is insufficient. The API must also accept a
pre-existing socket and expose its redirect-rejection path. It installs nothing. A
repository-controlled client is required; standard-library REST is approved,
but a custom RFC6455 stack is rejected. WebSocket execution must use the
separately proved compatible dependency or stop `UNSUPPORTED_INTERFACE` before
prompting.

The exact PASS markers are:

```text
TARGET_IDENTITY=PASS
ENDPOINT_POLICY=PASS
REDIRECT_SUPPRESSION_CAPABILITY=PASS
CREDENTIAL_PROMPT=PASS
CREDENTIAL_ACQUIRED=TRUE
REST_AUTHENTICATION=PASS
REST_CAPABILITY=SUPPORTED
WEBSOCKET_AUTHENTICATION=PASS
WEBSOCKET_CAPABILITY=SUPPORTED
READ_SCOPE=PASS
INSTANCE_REFERENCE_METHOD=OPERATOR_LOGICAL_LABEL
PRIVACY_VALIDATION=PASS
RESULT=PASS
ERROR_CODE=NONE
FAILURE_STAGE=COMPLETE
ROLLBACK_RECOMMENDED=FALSE
PE4_0B2A=COMPLETE
PE4_0B2B=NOT_STARTED
```

Every failure instead ends with `RESULT=FAIL`, one bounded `ERROR_CODE`, its
current `FAILURE_STAGE`, `ROLLBACK_RECOMMENDED=FALSE`,
`PE4_0B2A=NOT_COMPLETE`, and `PE4_0B2B=NOT_STARTED`, then stops. Codes/stages
are: `INVALID_ARGUMENTS/INPUT_VALIDATION`; `WRONG_TARGET`, `WRONG_OPERATOR`, or
`UNSUPPORTED_SHELL/TARGET_IDENTITY`; `SECURE_PROMPT_UNAVAILABLE` or
`AUTHENTICATION_UNAVAILABLE/CREDENTIAL_ACQUISITION`; `ENDPOINT_UNAVAILABLE`,
`UNAPPROVED_REDIRECT`, `PROXY_INFLUENCE_DETECTED`, or
`RESPONSE_TOO_LARGE/ENDPOINT`; `AUTHENTICATION_FAILED/AUTHENTICATION`;
`UNSUPPORTED_INTERFACE` or `INTERFACE_CAPABILITY_MISSING` at the applicable
REST or WebSocket capability stage; `INSUFFICIENT_READ_SCOPE/READ_SCOPE`;
`UNEXPECTED_SCHEMA` at the current capability stage;
`PRIVACY_CONTRACT_VIOLATION/PRIVACY_VALIDATION`; and
`UNEXPECTED_ERROR` at the current bounded stage. No failure triggers fallback.

### Authoritative sources

- Home Assistant developer REST API: https://developers.home-assistant.io/docs/api/rest/
- Home Assistant developer WebSocket API: https://developers.home-assistant.io/docs/api/websocket/
- Home Assistant authentication API: https://developers.home-assistant.io/docs/auth_api/
- Home Assistant permissions: https://developers.home-assistant.io/docs/auth_permissions/
- Core 2026.8.1 device registry source: https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/config/device_registry.py
- Core 2026.8.1 entity registry source: https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/config/entity_registry.py
- Core 2026.8.1 area registry source: https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/config/area_registry.py
- Core 2026.8.1 config-entry source: https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/config/config_entries.py
- Core 2026.8.1 WebSocket implementation: https://github.com/home-assistant/core/tree/2026.8.1/homeassistant/components/websocket_api

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

Preparation must prove an already-installed compatible `websockets` dependency.
It must install no package and must fail closed if that dependency is absent or
incompatible. REST alone is not assumed sufficient for registry metadata.

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

Repository-known facts now include the accepted deployment preflight and the
official 2a API contract above. No repository ingestion path from a Home
Assistant device, entity, area, or config-entry registry exists. Actual client
dependency availability and all 2b registry response schemas still require
separately prepared, fail-closed checkpoints; they must not be guessed.

## Access-authority matrix

| Source class | Classification | Contract |
|---|---|---|
| Authenticated supported REST API | SUPPORTED FOR 2a ROOT ONLY | `GET /api/` is frozen for authentication/API proof. The documented REST API exposes none of the required registries. |
| Authenticated supported WebSocket API | SUPPORTED FOR 2a AUTH ONLY | `/api/websocket` authentication is frozen. Source-level registry commands remain a version-pinned 2b candidate, not a public compatibility promise. |
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
mutation privileges cannot be required merely for convenience. PE-4.0B.2a uses
an operator-provided HA access/bearer token with the frozen non-echoing,
non-command-line invocation method above. Token generation remains outside
HIOC; failure to acquire the token safely stops.

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

PE-4.0B.2a deployment type, endpoint, authentication semantics, credential
injection, network policy, bounds, output, and STOP contract are frozen above.
The repository-controlled client is implemented but unexecuted. Separately
authorized source/deployment identity and credential-free dependency proof must
pass before live access. The 2b registry
schema/evidence tool and PE-4 implementation remain separate and not started.
