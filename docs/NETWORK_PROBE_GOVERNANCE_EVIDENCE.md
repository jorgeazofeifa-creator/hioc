# Evidence Report: Phase 7A Network Probe Source Governance and MQTT Health Hardening

Date: 2026-07-29

## Production trigger

PI5 changed from `192.168.100.152` to `192.168.100.251`. Runtime configuration was corrected, but the unmanaged network probe retained the old address for PI5 probing and inventory publication.

## Source intake

- Archive: `hioc-network-probe-source-intake-20260729-220644.tar.gz`
- Archive SHA-256: `74e7e251bd0848a0b87d2f314fd2d0958bd5c9730a8b6ff37fff449c1052bf6d`
- Captured script SHA-256: `edf6ad456292a0fb9441f09e7eb59fa02831cee46aa7071dcaa7b8d3eadc39a1`
- Captured host: `nutandpihole`
- Captured source: `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`
- Repository source: `pi4-tools/scripts/hioc-network-probe.sh`
- Production deployment path: `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`

The archive contained exactly the expected two regular files, had no unsafe paths or links, and was extracted outside the repository. Evidence confirmed no enclosing Git repository, the five-minute cron invocation, expected hashes, and both old hardcoded PI5 references. The captured script passed `bash -n`.

## Intended behavior and invariants

Existing probes, retained topics, counters, events, thresholds, payload schemas, names, roles, and logs are preserved. PI5 probing and inventory derive from required `HOME_ASSISTANT_IP`; neither production PI5 address is embedded in executable source; jq receives the address through `--arg`; credentials are never logged. Deployment excludes configuration, logs, and state.

Dashboard operational health uses a parseable last-success timestamp with a 12-minute threshold and two-minute future tolerance. Invalid, unavailable, unknown, empty, stale, and implausibly future timestamps are not Healthy. Historical failures remain visible evidence but do not determine current health.

## Repository validation

Status: **PASS**. Both shell sources passed Bash syntax validation. Six new focused tests passed. The full regression suite passed 197 tests with 7 environment-dependent skips. Git diff checks, endpoint/source searches, secret review, and documentation-link checks passed. Home Assistant YAML tests were included but skipped because PyYAML is unavailable in the bundled Windows runtime; operator-side Home Assistant validation remains required.

## Production validation

Status: **PENDING**. Codex did not access PI3 or PI5. Controlled deployment, hash comparison, MQTT/inventory evidence, Dashboard V2 deployment, and runtime UI validation remain operator tasks.

## Warnings

- Only `hioc-network-probe.sh` was captured. Remaining `pi4-tools` content is not governed here.
- The cumulative MQTT failure count must not be erased merely to make a dashboard green.
- Dashboard V2 deployment and runtime validation remain operator tasks.
- Repository source existence alone does not validate production.

Final repository result: **PASS**. Overall checkpoint: **OPEN, PRODUCTION PENDING**.

## Corrective checksum-governance checkpoint (2026-07-30)

The original report incorrectly recorded
`27e4dec6f4b42c6470d0486da37eed5c7f5fc6c5da58fb1b02d49e4534ff4310`
as the authoritative checksum. PI3 validation stopped before deployment, so no
production file was changed. The committed blob and PI3 working tree were
subsequently proven byte-identical. The actual SHA-256 of the committed Git
blob at commit `f195f823ff2353cf8260fcee1c8a98cde8b13c9a`, path
`pi4-tools/scripts/hioc-network-probe.sh`, Git blob
`d0deaa719826525b058235d57d7ef5eac3f9b21a`, is
`8737ed600270a846f2049843be7e309958d7f6f2ca696f9cba55dd3d0c098887`.

### Forensic conclusion: PROVEN ORIGIN

The authoritative blob is 12,805 bytes with 364 LF and zero CRLF sequences.
The Windows checkout is the same logical file after Git checkout conversion
to CRLF: 13,169 raw bytes with 364 CRLF sequences. Those Windows bytes hash
exactly to the incorrectly reported `27e4...` value. Converting the committed
blob to CRLF independently reproduces it. The raw worktree and blob are not
byte-identical, although `git hash-object` produces the same blob ID because
Git applies configured clean conversion. Missing/added final newline and UTF-8
BOM variants did not produce the incorrect value. The file did not exist in
the parent commit, history contains only its introduction in `f195f823`, and
the reflog did not identify an earlier committed version.

### Process failure analysis

Proven failures: the checksum came from raw Windows worktree bytes rather than
the final Git blob; it was manually transcribed into the operator command; the
report omitted the derivation command and blob ID; no test compared published
identity to raw committed bytes; and the deployment helper trusted worktree
identity rather than an approved commit. Repository PASS therefore contained
defective deployment evidence. Inferred from the absence of post-push
object-derived evidence: calculation was independent of final committed-object
verification, and final validation did not regenerate all evidence from
`origin/main`.

The failed PI3 validation is a successful safety stop. The false checksum is a
governance defect. Production deployment and the overall checkpoint remain
open. Repository PASS must be recorded only after the corrective commit is
pushed and evidence is regenerated from that exact `origin/main` commit.

## Endpoint Migration Audit

### Repository-wide search summary

A complete search of tracked source, tests, documentation, Home Assistant YAML,
Python, Shell, JSON, configuration examples, fixtures, and deployment tooling
found no active PI5 target literal in production logic or runtime configuration
templates. The later operator refinement contains the retired address only in
two fail-closed negative guards; it cannot be used as a probe target.

The old address is classified as follows. The tracked operator's two **Current
production logic** occurrences reject that value in `HOME_ASSISTANT_IP` and
retained inventory. They are correct negative guards, derive no endpoint, and
cannot publish probe state.

- `docs/HIOC_MASTER_PLAN.md`: **Historical reference** describing the migration.
- This Evidence Report: **Historical reference** describing and classifying the
  governed defect.
- `tests/test_network_probe_governance.py`: **Test fixture** occurrences used
  only in negative assertions that prohibit and constrain the literal.

The current address `192.168.100.251` occurs ten times:

- `docs/HIOC_MASTER_PLAN.md`: **Historical reference** in the migration record.
- This Evidence Report (two occurrences): **Historical reference** in the
  migration record and classification.
- `docs/INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md` (two occurrences):
  **Historical reference** recording the completed network change.
- `docs/NETWORK_FOUNDATION.md` (two occurrences): **Documentation** defining the
  current network contract.
- `docs/SYSTEM_REFERENCE.md`: **Documentation** describing the current topology.
- `tests/test_network_probe_governance.py` (two occurrences): **Test fixture**,
  used only in negative assertions that prohibit the literal.

There are zero active endpoint occurrences classified as **Current production
logic**, **Runtime configuration template**, or **Obsolete code**. The two
current-logic negative guards are not endpoint definitions.

### Every production endpoint reference

| Component | Endpoint behavior | Classification and correctness |
| --- | --- | --- |
| Network probe | Requires `HOME_ASSISTANT_IP`, assigns it to `pi5_ip`, uses that value for both ping checks and the legacy inventory record, and contains neither address literal. | Current production logic; correct after deployment; derives from the single runtime authority. |
| Incident Engine v2 | Reads `HIOC_LEGACY_BASE_TOPIC/network/pi5_status`; it does not resolve or contact PI5. MQTT broker connection uses the separate `MQTT_HOST` dependency. | Current production logic; correct status consumer; no independent PI5 endpoint. |
| Legacy incident engine | Reads the same configured legacy-topic `network/pi5_status`; it does not resolve or contact PI5. | Current production logic retained for compatibility; no independent PI5 endpoint. |
| Inventory generation | The governed probe publishes its legacy Pi5 inventory address from `pi5_ip`. Core Living Inventory has no PI5 address literal or independent PI5 endpoint. | Current production logic; probe-side record correctly shares `HOME_ASSISTANT_IP`. |
| Diagnostics and dashboards | Render incident and probe-status entities; no endpoint is contacted or defined. | Current production presentation; no independent PI5 endpoint. |
| Dependency graph and correlation | Consume inventory/status evidence; no endpoint is contacted or defined. | Current production logic; no independent PI5 endpoint. |
| REST sensors and ping sensors | No repository definition targets PI5. | Does not reference PI5. |
| MQTT publishing | Probe publishes the result; Incident Engine publishes correlated incident JSON. `MQTT_HOST` identifies the broker, not PI5 reachability identity. | Current production logic; separate configured dependency, no PI5 literal. |
| Home Assistant MQTT entities and template sensors | Consume retained HIOC incident topics and render fields; no endpoint is defined. | Current production logic; no independent PI5 endpoint. |
| Automations | React to incident entity state for notification/logging; no endpoint is defined. | Current production logic; no independent PI5 endpoint. |
| Deployment helper | Deploys the exact approved Git blob and does not define runtime endpoints. | Current production logic; no PI5 endpoint. |

The repository does not contain a tracked `toolkit.conf` template defining
`HOME_ASSISTANT_IP`; that file remains deliberately untracked runtime
configuration. Repository evidence from the prior checkpoint records that its
value was corrected. Consequently, within governed executable logic there is
exactly one PI5 endpoint authority: runtime `HOME_ASSISTANT_IP`, owned by
`toolkit.conf`, consumed only by the network probe. Topic selection is a
separate hierarchy: the probe publishes under `MQTT_BASE_TOPIC` and the
incident engines consume the corresponding `HIOC_LEGACY_BASE_TOPIC`.

### Incident publication path

1. `pi4-tools/scripts/hioc-network-probe.sh` pings `HOME_ASSISTANT_IP`, converts
   the result to `pi5_status`, and publishes the retained topic
   `home/infrastructure/pi4/network/pi5_status` under the default base.
2. `pi4/bin/hioc-incident-engine-v2.py` reads
   `<HIOC_LEGACY_BASE_TOPIC>/network/pi5_status` every scheduled run.
3. `pi4/lib/hioc/core/correlation.py` converts any value other than `online`
   into signal `pi5_offline` with evidence
   `PI5 / Home Assistant host is unreachable from Pi4`, then correlates it to
   title `Home Assistant host unreachable`.
4. Incident Engine v2 writes `state/incidents/active.json` and publishes it
   retained to `home/infrastructure/hioc/incidents/active`.

### Incident consumption path

`homeassistant/packages/hioc_incident_center.yaml` consumes the retained active
incident topic into `sensor.hioc_incident_active` and related status, severity,
reason, and recommendation sensors. `homeassistant/dashboards/hioc_dashboard_v2.yaml`
renders those entities on its incident and Diagnostics views. The separate raw
probe-status entity `sensor.pi4_network_probe_pi5_status` is referenced by the
storage-exported dashboard, but its Home Assistant MQTT entity definition is
not present in this repository; that presentation-only link cannot be proven
further from repository evidence.

### Remaining risks

- The audit proves repository content, not untracked production configuration
  or unmanaged Home Assistant entity definitions. Operator validation must
  still confirm `HOME_ASSISTANT_IP`, topic alignment, new retained probe state,
  and incident recovery without printing credentials.
- A successful probe run is required to overwrite the old retained
  `pi5_status`. Merely copying the corrected file cannot clear the incident.
- If another unrelated higher-ranked signal exists, correlation may display
  that incident after the false PI5 signal clears; this is not continued PI5
  endpoint generation.

### Deployment expectation

After governed deployment and one successful controlled probe run, the probe
will ping the configured current endpoint and overwrite retained
`network/pi5_status` with `online`. Incident Engine v2 runs every minute. With
no remaining actionable signal, it marks the incident recovering on the first
cycle and clears it after the configured two recovery-confirmation cycles,
then publishes the non-active document. Thus it clears automatically after
the retained status is overwritten and the recovery cycles complete; it does
not require a manual timeout or permanent reset.

Final conclusions:

1. After deployment, is there any known repository component that can still
   publish a false PI5 unreachable incident? **NO**.
2. Is the current dashboard incident fully explained by the undeployed probe?
   **YES**. The exact displayed evidence and title are generated only from the
   probe-owned retained `pi5_status`, and the stated production probe still
   targets the old address.
3. Can production deployment proceed safely after this checkpoint? **YES**,
   subject to the existing fail-closed operator validation and post-deployment
   retained-state/recovery checks.

## Deployment and Incident-Recovery Result Semantics

Deployment correctness and downstream incident recovery are separate
validation domains. Phase A is deterministic and fail-closed. Phase B begins
only after Phase A passes and observes downstream convergence for a bounded
period; it cannot reclassify a successful deployment as failed.

- **PASS:** Phase A deployment and Phase B recovery both validate.
- **PARTIAL PASS:** Phase A validates, but Phase B is delayed or inconclusive.
  Separate follow-up is required without rollback based solely on Phase B.
- **FAIL:** A deterministic Phase A invariant fails and the command exits
  nonzero. Rollback is considered only after a justified post-change failure.

The 190-second window is bounded evidence, not a recovery guarantee. Phase B
PASS requires a parsed read proving the false key and evidence absent. The
procedure reports successes, failures/timeouts, malformed payloads, last key,
last evidence state, and elapsed duration. The checkpoint remains open pending
operator evidence review. Endpoint Migration Audit conclusions are unchanged.
