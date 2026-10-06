# HIOC Compatibility Resilience and Dependency Drift Audit

## Authority, boundary and defect

Repository-only correction from clean synchronized main
`2c339bb3a597aaae152c3fb684c11b96eed9bfe9` (`PE-4: prepare bounded registry discovery`).
The first authorized 2b attempt failed safely because external HA Core version
was used as an exact runtime gate. The defect is
`EXTERNAL_SOFTWARE_VERSION_USED_AS_COMPATIBILITY_GATE_INSTEAD_OF_CAPABILITY_CONTRACT`.
The first failure is historical evidence, not permission to execute again.
No PI3/PI5/HA access, credentials, deployment, corrected 2b execution or PE-4.0C
occurs in this checkpoint.

The governed [registry](../governance/compatibility-contracts.json) and its
[explicit schema](../governance/compatibility-contracts.schema.json) use version 1.0.
Each row has exactly one primary class: A independently updated software;
B HIOC controlled dependency; C provenance/security identity; D supported runtime
family; E external protocol/data shape. Rows are contract families: utility and
standard-library members are enumerated below rather than invented as separate
version-pinned products. Related software and wire-data boundaries deliberately
have separate records (for example HA Core and its registry schema).

## Complete dependency matrix

Version discovery is optional and bounded. Required capability failure pauses
only the component named in the registry. Version drift alone can fail only
intentional controlled identities or a governed supported-family boundary.
Every matrix row carries owner, consumer, probe, security, isolation and remediation
fields in the machine-readable registry. Unobserved rows remain UNKNOWN.

| Dependency ID / name | Class | Policy | Required capabilities | Consumed boundary and unresolved proof |
| --- | --- | --- | --- | --- |
| `ha_core` / Home Assistant Core | A | capability-based | `version_metadata`, `authentication`, `device_registry`, `entity_registry`, `area_registry`, `config_entries` | Four approved read commands, strict JSON, mandatory field core and recognized types; unknown optional fields counted, never exposed. HA release token informational. |
| `ha_registry_schema` / Home Assistant WebSocket registry schema | E | capability-based | `correlated_results` | Integer correlation; one result per command; auth envelope; bounded arrays/objects; no unsafe widening. |
| `ha_yaml` / Home Assistant YAML and template/MQTT integration | E | capability-based | `yaml_templates` | HA package YAML, MQTT state/attribute keys, entity names, Jinja templates; ha core check is applicable execution probe. |
| `ha_config_path` / Home Assistant config mount and CLI | A | capability-based | `config_mount`, `core_check` | Configurable HA_CONFIG, readable/writable package directory and core-check command; OS version alone never gates. |
| `pihole_ftl` / Pi-hole FTL | A | capability-based | `lease_source` | FTL service name and optional package observation; ingestion shape isolated separately. No FTL API client exists here. |
| `pihole_leases` / Pi-hole/dnsmasq DHCP lease format | E | capability-based | `lease_columns` | Configured path; 3–5 whitespace columns; nonnegative expiry; MAC; IPv4; optional hostname/client ID. ISC/IPv6 unsupported. Empty alone is unknown, not format failure. |
| `nut` / NUT service and UPS observation | A | capability-based | `ups_status` | Current repository consumes systemd/dashboard status; no upsc invocation or UPS wire-port use found. Pure adapter separates unknown status from unavailable service. |
| `go2rtc` / go2rtc camera observation | A | informational only | `streams_object` | Current checkout contains dashboard entities, no standalone go2rtc HTTP caller. Governed external port 1986 remains informational contract pending integration, never changed to upstream default. No API request authorized. |
| `mqtt_transport` / MQTT broker transport | E | capability-based | `connack`, `publish` | MQTT 3.1.1 TCP, bounded CONNACK, retained QoS 0; configurable port default 1883. No TLS implementation in minimal publisher; configured secure transport requires separate reviewed support. |
| `mqtt_cli` / Mosquitto CLI utilities | A | capability-based | `publish_cli`, `subscribe_cli` | Configured host/port credentials; -C 1 retained retrieval, timeouts, byte payload shape. Version informational; no broker-version pin. |
| `windows_python` / Windows operator CPython | D | supported-line | `cpython_line` | CPython 3.13.x floats patch after capability probe;3.13.15 historical tested evidence. Manager resolution must select approved line. |
| `system_python` / System Python and stdlib | D | supported-line | `cpython_line` | CPython language floor3.10; production exact version unverified, not supported-line promotion. Validate imported APIs, subprocess, asyncio and filesystem capabilities. |
| `pe4_python` / Governed PE-4 CPython runtime | B | intentional exact pin | `interpreter_start`, `runtime_api` | CPython 3.11.2, aarch64/SOABI/prefix/tree exact approved construction; host interpreter/shared-library usability probed before import. |
| `pe4_websockets` / Governed websockets wheel and API | B | intentional exact pin | `import_api`, `bounded_connect` | websockets 16.1.1 exact governed wheel/distribution origin; async connect class, process_redirect, max_size, proxy controls and cancellation surface. |
| `pe4_packaging` / Governed PE-4 pip/setuptools lock | B | intentional exact pin | `locked_distributions` | Exact accepted pip/setuptools distribution versions originate digest-bound ActionD record; offline/hash-locked installation, no automatic upgrades. |
| `artifact_trust` / Git objects, wheel/data hashes and immutable evidence | C | security trust anchor | `identity` | Git blobs/full commits, SHA256 wheel/database/manifests, immutable D/E/F/G evidence. Cryptographic transforms of household IDs are separate privacy mechanisms, not version gates. |
| `openssh_trust` / Microsoft OpenSSH executable and SSH host/key trust | C | security trust anchor | `identity` | Pinned signed Microsoft executable hashes/signatures, host/key trust and explicit tool path. Servicing drift requires trust-anchor refresh, never automatic adoption. |
| `openssh_protocol` / OpenSSH execution/SFTP protocol | A | capability-based | `secure_transfer` | Required SSH options, noninteractive authentication, no forwarding, explicit known-hosts trust, fail-closed result handling. |
| `git` / Git CLI | A | capability-based | `object_commands`, `clean_sync` | Object commands, no-replace/filter semantics, clean index/worktree, synchronized branches; no exact Git executable version gate. |
| `bash` / Bash | A | capability-based | `bash_semantics` | Arrays/process substitution/pipefail/source and /dev/tcp where used. Windows WSL launcher does not resolve Windows paths like Git Bash; choose an applicable shell. |
| `powershell` / Windows PowerShell/Core | A | capability-based | `native_process` | Native argv/stdout/stderr/exit and direct Python invocation behavior; PowerShell5.1 stderr promotion recorded; no patch-version pin. |
| `python_manager` / Python Install Manager and WinGet | A | capability-based | `managed_line_resolution` | Official package ID provenance; list --one --format=exe/json --only-managed3.13; disable automatic install; manager default is not a runtime compatibility promise. |
| `iproute` / iproute2 ip/ss | A | capability-based | `address_route_neighbor`, `socket_columns` | Consumed ip -o -4 addr, route default, neigh token semantics; ss -ltnup endpoint columns; no exact utility version. |
| `nettools` / Legacy arp fallback | A | capability-based | `arp_columns` | arp -an fallback host/IP/MAC parser; failed collection distinct from empty neighbor set. |
| `systemd` / systemd/systemctl service observation | A | capability-based | `unit_columns` | list-units --type=service --all --no-pager --plain; unit/load/active/sub columns; configured unit names may differ by distribution. |
| `scheduler` / cron/crontab/flock | A | capability-based | `scheduling`, `locking` | Cron line semantics and nonblocking flock; locks prevent overlapping compatibility-state writers when configured. |
| `jq` / jq JSON CLI | A | capability-based | `json_filter` | Required jq filters, -e/-r/-n and schema fields; exact implementation version unnecessary. |
| `curl` / curl HTTP CLI | A | capability-based | `http_options` | Consumed bounded timeout/status/body behavior; transport failure distinct from API shape; no automatic secret/body diagnostics. |
| `openssl` / OpenSSL CLI and SSL library | A | capability-based | `crypto_api` | Invoked options/imported SSL API as consumed; no direct executable version gate discovered. |
| `dns_tools` / DNS dig/nslookup/host and libc DNS | A | capability-based | `dns_answer` | Query status/answer/time syntax and socket reverse resolution; no DNS listener version gate. |
| `snmp` / SNMP snmpget | E | capability-based | `sysdescr` | SNMP v2c sysDescr OID and -Oqv output; secret community excluded from compatibility status. |
| `ping` / ICMP ping | A | capability-based | `ping_result` | -c/-W, exit status, packet-loss and RTT parsers; active discovery remains separately governed. |
| `linux_metrics` / Linux df/free/vcgencmd/proc/sys/os-release | A | capability-based | `metrics_shape` | df -P/free fields, measure_temp token, proc/sys Linux paths; unavailable board-specific metrics remain isolated. |
| `dpkg` / Debian dpkg-query/apt | A | informational only | `package_metadata` | dpkg-query -W -f=${Version} informational; missing distro package tool does not mean version incompatibility. |
| `rsync` / rsync deployment | A | capability-based | `archive_exclusions` | Archive/exclusion/backup semantics preserve runtime, manufacturer data, state; version informational. |
| `filesystem` / POSIX/Windows filesystem and process facilities | A | capability-based | `atomic_state`, `private_binding` | Atomic replace for HIOC state, no-replace link for immutable evidence, permissions/UID/GID/sticky tmp, no-follow descriptors; Windows equivalent adapters are not production certification. |
| `linux_utils` / Linux coreutils/findutils/text/archive commands | A | capability-based | `utility_semantics` | Exact consumed options/output in source; classify utility availability/shape, not OS/distribution release. GNU-specific -c/-f/-T and procfs semantics must be probed on execution host. |
| `pyyaml` / PyYAML optional validator | A | capability-based | `yaml_parse` | Optional import/parser path in validators; missing parser explicitly skipped or unknown, never HA compatibility proof. |
| `internal_schemas` / HIOC checked-in schemas and protocol versions | B | internal schema | `schema` | HIOC-owned schema IDs/versions/parser identity stay exact; additive external contract handling does not widen internal schemas. |
| `manufacturer_data` / IEEE RA CSV vendor dataset and HIOC database | E | capability-based | `csv_columns` | Three source CSV contracts, UTF8/field/assignment semantics; generated vendored database trust hashes remain governed separately. |
| `ha_frontend` / HA frontend custom cards | A | capability-based | `card_resources` | Mushroom and mini-graph-card resources in historical dashboard; no version gate; rendering capability not proven by repository tests. |
| `upstream_entities` / External HA entity providers and toolkit payloads | E | capability-based | `payload_fields` | Existing external entity/state/topic names from toolkit/Frigate/Ring camera and UPS provider; numeric/status keys consumed; changes affect corresponding presentation/integration only. |

## Exact versions, pins and retained identity rationale

The [complete per-file/per-line inventory](../governance/compatibility-audit.json)
records version/pin candidates, literal versions, exact SHA/Git identities,
policy classifications, executable versus historical/test context, Python imports,
process call sites and source SHA256 coverage. Pattern matches are an audit index;
they are not proof of semantic classification. Source/caller review distinguishes
an external gate from internal version evidence, test constants and privacy hashes.
Every repeated immutable evidence digest remains at its original source; the
inventory references each occurrence rather than silently refreshing it.

| Exact value or identity family | Primary class / disposition | Rationale |
| --- | --- | --- |
| HA Core 2026.8.1 | A / baseline provenance only | Historical source review; runtime equality gate removed. New versions must pass auth and all four schemas. |
| CPython 3.11.2; CPython 311; aarch64; `cpython-311-aarch64-linux-gnu` | B / retained exact isolated runtime | Accepted D/E construction, prefix, ABI, platform and complete-tree identity. Host capability break is separate from version drift. |
| `websockets==16.1.1` and complete wheel filename/platform tags | B / retained exact wheel/distribution | Reviewed API surface, offline reproducibility and accepted runtime tree. Version and origin cannot float. |
| pip 23.0.1, setuptools 66.1.1 where recorded in accepted/synthetic construction | B / retained accepted packaging identity | Actual accepted distribution set is digest-bound Action D evidence; no package refresh or substitute wheel. Synthetic records do not establish a live packaging observation. |
| manylinux2014/aarch64, manylinux_2_17/2_28 and CPython ABI wheel tags | B / retained compatibility construction contract | Platform tags and ABI selection define the approved artifact; not exact host OS release gates. |
| Windows CPython 3.13.x, reviewed patch 3.13.15 | D / supported line; patch floats | Existing major/minor execution probe governs selection; reviewed patch is evidence, not an equality gate. |
| CPython floor3.10, tested 3.12.13, observed 3.14.7; production exact unverified | D / policy/evidence | Floor does not confer operational support.3.14 is outside the approved Windows line. No supported production line is invented. |
| HIOC VERSION manifest1.0.0; incident1.2.0; correlation2.0.0; forecast1.1.0; dashboard2.0.0; schema3; mqtt_api2; build2026.07 | B / internal release/schema identities | Current HIOC component protocols are governed contracts, not external software releases. Existing exact internal validation remains. |
| Internal asset/enrichment/manufacturer/PE2/PE3/PE4/schema/lock/parser versions (all occurrences in inventory); new compatibility1.0 and 2b report1.1 | B / internal schema | Exact producer/consumer semantics and provenance; additive HA fields do not widen internal evidence schemas. |
| Manufacturer dataset2026-08-11-r1 and generated database/manifest identities | C / source evidence and accepted immutable artifact | Dataset selection is explicit provenance. IEEE CSV columns are E structural contracts; downloaded bytes never auto-replace trusted data. |
| SSH client SHA256 `786ff14be7cd652b2b9770a57e9b1aa5e03a052ce3a3d641fb4760c0ff3fde05`; keygen SHA256 `47f009c35523b6997aff0f0528dae84f1545465479d722292499941cd5cb83b5` | C / retained executable trust | A servicing update requires governed identity review. The new executable is never automatically accepted. |
| SSH public/host fingerprints, signed publisher identity, ACL/known-host/key bindings | C / retained trust | Prevent replacement and wrong-target access. Diagnostic classification does not refresh keys or trust. |
| All Git commit/blob IDs, SHA256 wheel/requirements/runtime-tree/schema/source/evidence/database bindings | C / retained immutable provenance | Reproducibility, evidence closure and chain of custody. New correction record binds new source; original preparation record remains byte-identical. |
| MQTT 3.1.1, QoS 0; SNMP v2c; IPv4; HTTP/WS numeric target; protocol flags/OIDs | E / required wire behavior | Protocol selection, correlation and fields are capability contracts, not broker/server executable release gates. |
| Default MQTT1883, governed HA8123, SSH22, go2rtc1986, fixed governed paths/service names | A/E consumer boundary (or C target trust) | Configuration/target identity and port semantics; no claim that upstream default equals local governed value. Missing/moved path is availability or contract failure. |

No external HAOS/Supervisor version-specific caller was found; their versions
cannot gate PE-4. No Unbound executable/API consumer was found, so no dependency
record or invented probe was added. Port1986 is the user-governed go2rtc contract;
this checkout has no standalone HTTP client that establishes it live.

## Removed gate and replacement contracts

Only the HA greeting/auth version equality gate was an independently updated
external exact-release gate. `ha_version` is now an approved bounded numeric
release token (including recognized prerelease suffix); malformed or inconsistent
metadata fails safely.2026.8.1 remains source-review provenance. Unknown optional
envelope/record fields may be structurally reduced; required field removal/type
change, unsafe values, excess size, command removal or authorization failure
still fails closed. One connection sends exactly:

1. `config/device_registry/list`
2. `config/entity_registry/list`
3. `config/area_registry/list`
4. `config_entries/get`

Required structural validation, bounded strict JSON, result correlation,
permission classification and privacy reduction replace external release equality.
No fallback, subscription, extra command, new credential path or automatic source
repin is introduced. Evidence schema 1.1 adds only sanitized compatibility metadata.
[Correction bindings](../governance/pe4/pe4-0b2b-compatibility-correction.json) are
current; [original preparation](../governance/pe4/pe4-0b2b-discovery-preparation.json)
remains immutable historical provenance with its original schema/source hashes.

No other external version-only runtime gate was found. Existing supported-line,
controlled-runtime, internal-schema and cryptographic equality checks remain.
New capability observations cover HA commands, lease shape, MQTT transport,
CPython family/floor, pure NUT/go2rtc structural adapters and isolated runtime
startup/import/API usability. The registry records remaining operator/OS/tool
contracts without inventing successful runtime observations.

## Integration and operator findings

Pi-hole: configured `/etc/pihole/dhcp.leases` and alternate sources use the existing
3–5-column parser (expiry/MAC/IPv4/optional hostname/client ID). Lease ingestion
reports found as compatible; malformed/partial/unsupported as incompatible;
missing/unreadable/I/O error as unavailable. Empty is UNKNOWN because zero leases
cannot establish format compatibility; it does not assert an update or inventory
failure. Version collection is optional, and the current producer does not
establish FTL version. Private lease values never enter compatibility state.
Service names and configured paths are capability boundaries; there is no FTL API
caller. DNS status/answer/time and reverse-lookup parsing are audited separately.

NUT: this checkout consumes systemd service/dashboard entities, not `upsc`, a UPS
wire port or a standalone variable fetch. The pure supplied-text adapter recognizes
OL/OB/LB/HB/RB/CHRG/DISCHRG/BYPASS/CAL/OFF/OVER/TRIM/BOOST/FSD in `ups.status`.
Unknown tokens are an explicit structural incompatibility, transport absence is
unavailability, and neither claims a software update. This adapter does not prove
live variable availability. Phone-notification semantics remain separately planned.
[NUT protocol source](https://networkupstools.org/docs/developer-guide.chunked/apas02.html)
defines status as token data; the adapter deliberately accepts only its reviewed set.

go2rtc: repository evidence is dashboard entities, not an API caller. Governed
port 1986 is preserved as informational. A pure adapter checks a supplied mapping
of stream name to object; optional object fields may expand, list/type replacement
fails. It neither requests `/api/streams` nor certifies endpoint/authorization/
port reachability. Those are explicitly deferred integration proofs.
[Upstream handler source](https://raw.githubusercontent.com/AlexxIT/go2rtc/master/internal/streams/api.go)
is reference context only; it does not override the local1986 contract.

MQTT: minimal Python client selects3.1.1 TCP, default configurable 1883, clean
session, retained QoS 0. Fragmented CONNACK is now correctly assembled; invalid
header/length/session flags/return code identifies MQTT incompatibility; premature EOF is transport unavailability.
No exact broker/client version is required. `mosquitto_sub`/`mosquitto_pub` options,
-C1 retained retrieval and bounded subprocess behavior remain operator capabilities.
There is no TLS implementation in this minimal publisher; secure transport needs
separate governed implementation. Successful send proves local transport write,
not broker delivery (QoS 0 has no acknowledgement). MQTT failures preserve local
state and isolate publication. Both platform and inventory producers update the
shared transport observation; unexpected local probe errors remain UNKNOWN. Compatibility payload excludes connection secrets.

Python/runtime: no code contradicts the supported-line/patch-evidence distinction.
The platform CPython observation proves implementation/language floor only.
Operational support is still owned by PYTHON_RUNTIME_COMPATIBILITY.md and its
support record. Exact isolated 3.11.2/websockets 16.1.1 checks are intentional;
bounded startup/import/API adapters distinguish missing interpreter, unusable
host ABI/API and frozen identity drift. They never repair/install or run remotely.
Execution of an approved runtime probe must follow its trust gates. Startup or
loader failures before the producer starts require operator-side diagnosis;
this checkpoint does not pretend an unstartable process can publish its own state.

SSH: existing signed/hash, key, fingerprint, known-host, ACL and explicit-path
checks are retained. Action B terminal diagnostics now explicitly classify the
existing precise executable/key/host mismatch codes as TRUST_ANCHOR_CHANGED,
without asserting servicing caused them. Missing tool is unavailable. Historical
D/E/F/G implementations/evidence are unchanged. Git object/clean/sync/no-replace
behavior, Bash arrays/pipefail/process substitution and PowerShell native argv/
stderr/exit handling are capability contracts. WindowsApps WSL launcher resolution
is not equivalent to Git Bash for Windows paths; validation selects Git Bash.
Official Python Install Manager package/resolution and no-auto-install behavior
remain required operator prerequisites, independent of its default interpreter.

OS/utilities: reviewed command families include ip/ss, arp, systemctl, cron/
crontab/flock, jq, curl, OpenSSL/stdlib SSL, dig/socket DNS, snmpget, ping, df/free/
vcgencmd, dpkg-query/apt and rsync. Coreutils/findutils/text consumers include cat,
cp/mv/ln/rm/mkdir/chmod/chown, stat/readlink/realpath, id/hostname, date/sync,
sha256sum, find/xargs, awk/sed/grep, cut/sort/uniq/head/tail/tr/tee/paste, dirname/
basename, tar/gzip, timeout and shell builtins. Required GNU flags/column semantics
are contracts (for example stat-c, find-printf, mv-fT, rsync exclusions), not OS
release gates. `/proc`, `/sys`, `/etc/os-release`, UID/GID, aarch64/SOABI, symlink/
no-follow/atomic replace/hard-link/fsync/private modes and explicit executable
paths are audited. Board metrics can be unavailable independently. Live Linux
capabilities cannot be certified on this Windows repository-only checkpoint.
Optional PyYAML, IEEE CSV columns, upstream toolkit/Frigate/Ring/UPS entities,
Mushroom and mini-graph-card resources are recorded; frontend rendering and HA
core-check require separately authorized host validation.

## Central status, persistence, privacy and isolation

`pi4/lib/hioc/core/compatibility.py` owns assessment and sanitized observations.
`state/platform/compatibility.json` uses the existing StateStore temporary-file /
atomic replace behavior, private mode0600 and a bounded exclusive writer lock.
It is not an immutable evidence file and does not add a durability/fsync guarantee
beyond the existing store. All writers merge observations; unknown IDs/raw keys
are discarded, only fixed registry metadata and bounded numeric versions survive.
IP addresses, MACs, URLs, household names, credentials and raw response/output
bodies are excluded. Existing immutable 2b evidence still uses its stronger
non-overwriting, fsync, result-last publication contract.

The existing platform collector publishes retained
`<HIOC_BASE_TOPIC>/platform/compatibility`, includes its summary in platform/status,
and preserves local authoritative state on MQTT failure. Inventory supplies lease
status from its existing snapshot; it does not perform another DHCP read.
The prepared 2b producer can record sanitized HA/runtime failures only within its
existing authorized execution; this checkpoint does not execute that path.
A compatibility framework failure cannot turn valid inventory/version telemetry
into a global integration failure. The HA package adds a compatibility sensor;
no dashboard redesign or phone notification behavior changes.

Summary fields: status, updated, overall_compatibility, dependency_count,
compatible_count, compatible_updated_count, degraded_count, incompatible_count,
unknown_count, trust_anchor_changed_count, unavailable_count, affected_components,
summary. Individual rows add observed/previous/last-known compatible version,
baseline, capabilities, failed capability, first detection, likely update flag,
affected component, recommended action and diagnostic. The explicit status schema
is [compatibility-status.schema.json](../governance/compatibility-status.schema.json).

States: COMPATIBLE passes required capabilities; COMPATIBLE_UPDATED additionally
records differing version with passing capabilities; UNKNOWN lacks fresh proof;
DEGRADED fails optional capability only; INCOMPATIBLE fails a required contract;
TRUST_ANCHOR_CHANGED rejects frozen identity drift; DEPENDENCY_UNAVAILABLE cannot
reach/execute/read the dependency. Aggregate severity is summary only. Unknown
rows do not mark unrelated components failed. Entries older than 36hours lose
current proof and become UNKNOWN while preserving last-known-compatible history.

Last-known-compatible is updated only after required success (including optional
degradation). Failure stores the current observation separately. First detection
is stable while version, failure and status remain the same across restarts.
Likely update break requires previously successful non-secret version A, current
version B, A!=B and current required failure. Baseline provenance alone, unchanged
version, missing version or connectivity failure never establishes update cause.
Reading existing state is not a new probe or new compatible timestamp.

Example fixed diagnostics (versions/capabilities are sanitized):

- `Likely update compatibility break: Home Assistant Core changed from 2026.8.1 to 2026.10.1; capability entity_registry failed. PE-4 Home Assistant Association is isolated.`
- `Compatibility trust change detected: Microsoft OpenSSH executable/key/host identity requires governed review. Action B is blocked; the new identity has not been trusted. No software update cause is established.`
- `Dependency compatibility failure: Pi-hole DHCP lease representation; capability lease_columns failed. passive DHCP inventory is isolated. No software-version change has been established.`

HA incompatibility isolates association; camera/NUT issues isolate their consumers;
MQTT affects publication rather than erasing authoritative local artifacts.
Future dashboard/notification checkpoints may consume this stable sensor/topic;
severity grouping, quiet periods and phone wording remain deferred.

## Historical execution evidence and lifecycle

First 2b: RESULT=FAIL, ERROR_CODE=UNSUPPORTED_HA_DEPLOYMENT,
FAILURE_STAGE=HA_DEPLOYMENT_DISCOVERY, PE4_0B2B=NOT_COMPLETE.
User-supplied evidence directory `/tmp/hioc-pe4-ha-discovery-22be880b`:
report SHA256 `efd3aa0cc2f5bc00a459a0c05055ac14e5a9a7ab6cc13aeeb34aa9aa616cb087`;
result SHA256 `1e11b6e512db860a8f9b2b6af1723c6aabafd75968d7fd643c891144a7a72195`.
These references are preserved without remote reading or mutation.

D/E/F/G PASS/CLOSED; E handoff ACCEPTED; 2a PASS/CLOSED; first 2b ATTEMPTED /
NOT COMPLETE; corrected 2b NOT STARTED; 0C NOT STARTED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED. Future execution needs separate authority,
current correction source/framework bindings and all existing pre-token gates.

## Validation boundary

Synthetic tests cover drift/capability combinations, absence versus failure,
additive schema, removed/type-changed fields, command removal/permissions, trust
and frozen identities, Python patch float/family rejection, MQTT framing, lease/
NUT/go2rtc adapters, isolation, persistent history/first detection, privacy and
retained publication. Release/install/upgrade, PE-4 and platform regressions,
source compilation, shell syntax and diff review are required before commit.
The full suite runs once at the final source boundary. Skips are recorded as
unverified platform paths, never production certification. No actual HA, UPS,
camera, broker or Linux-host compatibility success is claimed here.

## Audit inventory interpretation

The scanner covers every tracked/nonignored preparation text file except its
own generated inventory, this explanatory report and the registry used to classify
matches. All covered files receive SHA256 and dependency/call-site review indexing.
No binary/non-UTF8 input remains outside text review. Imports are standard library,
HIOC modules, the governed websockets API, or optional PyYAML; no additional
third-party Python package was found. Static literal process executables are
vcgencmd, bash, ip, ping, systemctl, ss, dpkg-query, snmpget, cat, arp, git,
powershell.exe, cmd.exe, rsync, ./bin/python, /usr/sbin/ip, /usr/bin/python3 and
/usr/bin/git. Dynamic commands were reviewed at their callers (including MQTT
CLI and governed runtime subprocesses); dynamic dispatch is not proof that the
execution host supplies the capability.

Numeric candidate literals in the audit include 1.0/1.0.0/1.1/1.2.0/2.0/2.1/2.6/
3.1/3.1.1/3.3 (internal/protocol/historical/test contexts); 3.10/3.11/3.11.2/3.12/
3.12.13/3.12.14/3.13/3.13.15/3.13.16/3.14/3.14.1 (runtime policy, tested evidence or synthetic drift); 16.1.1/
23.0.1/66.1.1 (controlled distribution evidence); 2026.8.1/2026.8.2/2026.10.1
(HA baseline or synthetic drift). 15.0/5.0/90.0 are bounded timeout constants,
not executable release pins. The per-site inventory provides precise path/line/
policy/context for each occurrence and records every matched 40/64-character
identity literal. Numeric regex candidates are deliberately not advertised as
independently updated external release gates. Internal VERSION manifest values
and schema integer versions are explicitly classified in the pin table above.

The manually reviewed dependency families encompass every executable, API,
protocol, consumed path/output/data format and ABI found in this checkout.
Zero unclassified families does not mean zero unresolved live capabilities:
operator prerequisites, Linux host facilities, HA package/rendering, upstream
entity providers, NUT/go2rtc APIs, TLS and production runtime support still require
authorized host evidence. The registry leaves those current observations UNKNOWN.

Current correction source/schema/framework hashes bind canonical Git LF bytes,
which must match actual Linux release-source bytes exactly during a future
authorized pre-token review. New governed artifacts declare LF in .gitattributes.
Unmodified historical Windows worktree CRLF files retain their existing bytes;
Git clean-object identity confirms unchanged source independently of checkout
line endings. Audit coverage SHA256 describes this Windows worktree observation.

Validation repair: the first whole-suite run on CPython 3.12.14 exposed two
older enrichment assertions that required exactly seven MQTT topics. Those
assertions now verify the eighth compatibility topic and its privacy boundary;
private enrichment and public inventory remain unchanged. Final validation
rechecks the corrected boundary rather than accepting the failed run.

## Final acceptance evidence - 2026-10-06

- Baseline main/local-origin/direct-remote: 2c339bb3a597aaae152c3fb684c11b96eed9bfe9.
- Final complete suite: CPython 3.12.14; 1362 tests run;1337 passed;25 platform skips; PASS; 257.115 seconds.
- Focused affected contracts: 313 tests; PASS; 3 platform skips.
- Preliminary full run: 1360 tests; two old seven-topic assertions failed and were corrected; the final complete run above is the acceptance result.
- All 143 Python sources compile in memory; all JSON parses; release validation PASS;
  all 26 shell scripts pass syntax. Release script's python3 alias check is skipped
  on this Windows shell; separate source compilation covers every Python file.
- Inventory: 257 source files, 3708 classified findings, 2539 version/identity candidate references,
  1081 imports,185 process sites; 42 unique dependency families; no unclassified
  family after caller/source review. Static coverage hashes were verified.
- Original 2a client/preparation/closure and protected D/E/F/G/runtime/lock/source-review
  objects retain 11 checked original canonical Git identities. Current correction
  source/schema/framework bindings pass. No Git operation was in progress.
- Exact changed-file review and git diff --check PASS. Existing ResourceWarnings
  from historical test file handles do not indicate a runtime capability proof.
- No PI3/PI5/HA access, credential use, deployment, corrected 2b execution, 0C or rollback.

## Exact changed files

Paths below are relative to the sole authorized repository
`C:\Users\JorgeAzofeifaCastill\Documents\HA\hioc`.

- `.gitattributes`
- `DECISIONS.md`
- `docs/CHANGELOG.md`
- `docs/COMPATIBILITY_RESILIENCE.md`
- `docs/HIOC_MASTER_PLAN.md`
- `docs/OPERATIONS.md`
- `docs/PE4_REGISTRY_DISCOVERY_PREPARATION.md`
- `docs/PYTHON_RUNTIME_COMPATIBILITY.md`
- `docs/SYSTEM_REFERENCE.md`
- `governance/compatibility-audit.json`
- `governance/compatibility-contracts.json`
- `governance/compatibility-contracts.schema.json`
- `governance/compatibility-status.schema.json`
- `governance/pe4/pe4-0b2b-compatibility-correction.json`
- `governance/pe4/pe4-0b2b-discovery-report.schema.json`
- `homeassistant/packages/hioc_platform.yaml`
- `pi4/bin/hioc-inventory-engine.py`
- `pi4/bin/hioc-platform-status.py`
- `pi4/lib/hioc/core/compatibility.py`
- `pi4/lib/hioc/inventory.py`
- `pi4/lib/hioc/mqtt.py`
- `tests/test_compatibility.py`
- `tests/test_hostname_enrichment.py`
- `tests/test_pe4_action_b_transfer.py`
- `tests/test_pe4_ha_registry_discovery.py`
- `tools/hioc-compatibility-audit.py`
- `tools/hioc-pe4-artifact-transfer.py`
- `tools/hioc-pe4-ha-registry-discovery.py`

The final index additionally includes numeric release observations in prose/
tables without requiring a variable named version. Its broad numeric candidates
include timeout/measurement constants; these are not asserted to be executable
release gates. This read-only index refinement is syntax-checked and executed;
production and test sources remain at the final accepted boundary.
