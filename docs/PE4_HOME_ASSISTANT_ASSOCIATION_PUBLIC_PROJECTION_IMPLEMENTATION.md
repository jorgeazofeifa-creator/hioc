# PE-4 Home Assistant Association Public Projection Source Implementation

Source Implementation: **IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS**.
Preparation: **PASS/CLOSED**. PI3 POSIX Source Validation: **NOT STARTED / PREPARED
FOR SEPARATE AUTHORIZATION**. Deployment and Production Execution: **NOT STARTED**.
This is repository source work, not deployment, actual POSIX validation or a
production readiness closure. PE-4 remains NOT COMPLETE; Phase 7A ACTIVE;
PE-5 NOT STARTED; rollback NOT PERFORMED. No production system was accessed.

## Authority

Starting main/origin/main: eda070d4b06ccd7f562a74e1cb6b42cb5c630d67, subject
PE-4: prepare association public projection, parent debe1ae485cf6b88839f9f8f2fbb071835deda05.
Origin fetched; exact branch/identities/subject/parent, clean 0/0 and no active Git
operation verified before changes. Preparation record/schema/document retain their
exact hashes. Its predecessor test remains Git-bound; only current-stage assertions
advance to the governed implementation identities and lifecycle.
The private producer, private schema 1.1, adapter entrypoint, scheduler/credential
artifacts, HA packages/dashboards and generic deployment scripts stay byte-unchanged.
Operator-supplied PI3 source review and crontab hash
8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71 are supplied authority,
not Codex observations. Both recurring schedules remain active and unmodified.

## Implementation and privacy

The inventory engine remains the sole public writer. A local stripping function
runs independently of optional imports: copy prior devices without home_assistant
before discovery, then strip current discovered devices before optional attachment.
The helper is imported only inside a contained try boundary after identity and
private internal-field removal, before the first public inventory write.
Import/read/parse/validation/derive failure logs only an allowed fixed local enum,
omits all HA objects and allows base inventory to continue. No exception text,
private values or public aggregate appears. Identity, observation/liveness, health,
incidents, Assets, topology and service ownership remain unchanged.

The helper separates strip_inventory, SecureReader.snapshot, load_contracts,
derive_projection, validate_public and attach_projection. It builds every candidate
before attachment and preserves current device order. Active association stable IDs
intersect current inventory IDs; missing devices are skipped, never created.
Duplicate current IDs invalidate optional projection. Binding history never projects.
Nonassociated devices omit home_assistant; no associated=false negative observation.

Exactly five required fields in a closed object:
associated=true; association_basis=strong_mac from unique_mac;
entity_count=len(validated retained entities), integer 0..65536;
integration_domains=unique lexicographically sorted config_entries[].domain ONLY,
max 4096 strings, length 1..64, exact lowercase technical pattern;
has_area_candidate=boolean validated non-null relationship presence.
No entity-platform fallback, IDs, names, areas, timestamps, metadata, history,
credentials or unknown values. Private privacy validation applies first; independent
public validation checks the exact closed shape, types, limits, sorting and privacy,
including rejection of full 12-hex compact MAC-like domains. INCOMPLETE supporting
relationships preserve a valid strong association and use only safely retained members.

## Validation identity and side-effect safety

Before any private module execution, securely read and SHA-256 verify the exact
private module (9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1),
private schema (5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d)
and new public schema. Execute only the verified immutable module bytes, avoiding a
second pathname import race or a cached alternate validator. The module's established
pure strict_json/check_schema_contract/validate_state/validate_privacy functions
are reused; the private validator is not forked. Public validation is independent.
No private runtime, network, credential, compatibility, recovery or publication API runs.
The private module imports websockets only in its uncalled network function.
New helper dependencies are standard library; POSIX imports are inside native paths.
Windows import and pure functions work without fcntl or Linux flags. Inventory keeps
its existing interpreter. Actual PI3 interpreter compatibility remains a required gate.

## Secure coherent reader

NativeReadFS mirrors accepted descriptor-relative no-follow/security semantics.
SecureReader pins the existing hierarchy from / through home/jazofv1/hioc to the
associations directory; no creation. Root/jazofv1 ownership, no group/world writes,
exact private owner/group, association directory 0700, state/lock regular 0600 and
link count one are required. NSS account/group readers are restricted as in the
accepted security contract. Access ACL permits only the exact mode-equivalent
three-entry ACL; default/extended ACLs and indeterminate xattr errors fail closed.

Use existing lock read-only/no-follow with LOCK_SH|LOCK_NB, no wait/retry/create.
While held: recheck hierarchy and lock binding, inspect bounded namespace before
and after copy, reject all txn/done prefixes including malformed names, lstat/open/
fstat agreement, size <=16 MiB, one complete bounded read, unchanged descriptor and
named file fingerprint, and final security/binding checks. Enumeration consumes at
most 4096 accepted entries plus one excess probe. No transaction content is opened.
A two-second monotonic internal copy deadline has checkpoints; filesystem I/O
cannot promise a universal wall-clock bound. All paths attempt lock release and
close every descriptor, including read, security, binding and unlock failures.
JSON, schema, semantics and derivation occur only after lock release. Later producer
replacement does not invalidate the copied committed snapshot. Producer exclusive
nonblocking locking stays unchanged. Busy reader omits projection; producer may
skip a briefly contended slot and retain private LKG until the next natural slot.
No forced retry or new scheduler. Existing outer inventory lock ordering has no
cycle because the adapter never acquires the inventory lock.

Only fixed omission enums: OMITTED_UNAVAILABLE, OMITTED_BUSY, OMITTED_UNSAFE,
OMITTED_INVALID, OMITTED_INCOHERENT, OMITTED_INTERNAL. Invalid optional metadata
never reaches the engine's global exception-text handler. Private LKG is untouched;
current public projection availability is distinct and never retains stale objects.

## MQTT, timing and future deployment

Inventory schema remains 1.0. Optional fields flow only through existing inventory
and inventory/devices payloads. Services/topology/dependencies/summary/status,
capabilities and platform/incident payloads remain unchanged. Retained QoS 0,
one connection, authoritative local files before MQTT and transport failure behavior
are preserved. Sequential local-file/topic writes are not newly atomic.
Existing HA inventory attributes carry nested devices; no package or UI change.
Normal inventory 0/30 and association 5/35 imply 25 minutes slot-to-next-inventory
lag; delayed/failed cycles have no hard guarantee and no liveness implication.

Deployment remains separate. Generic release/install/upgrade/rollback tools are
not authorized for projection deployment: non-atomic copying, cron mutation and
immediate inventory execution require a later narrow governed deployment path.
Future inventory quiescence/drain, helper and contract first, engine last, coherent
set verification and exact schedule restoration remain required. Association may
remain active only with its module/schema/runtime/lock contract unchanged. No such
maintenance, install, scheduler mutation or production execution occurred here.

## Committed future read-only source validator

The tool accepts only --source-commit with an exact 40-hex implementation commit;
no fixture, production path, credential or recovery switches. Run later with
python3 -I -B in /home/jazofv1/hioc-release-source as jazofv1 on nutandpihole.
Its own execution requires separate authorization after source sync and review.
Git identity checks are local/read-only with GIT_OPTIONAL_LOCKS=0 and fsmonitor
disabled. Exact clean main/origin identity and no Git operation are required.
The canonical implementation record/schema binds current artifact hashes/blobs.
Execute helper bytes from that exact Git commit, securely verify source and deployed
private identities, obtain a coherent private snapshot read-only, validate it and
read only current public inventory to reject any preexisting home_assistant key.
Derive a candidate in memory without attachment, engine execution, public writes,
MQTT, HA, credential, adapter, cron or private-state mutation. Recheck source authority.

Output is fixed sanitized key/value fields, <=8192 bytes, no IDs/domains/areas/raw
JSON/MAC/IP/hostname/private exceptions. PASS returns 0; busy means INCOMPLETE,
ASSOCIATION_BUSY, return 2 and STOP; other failure returns 1 and a closed error.
Every result includes STOP_REQUIRED=TRUE. No retry/repair. Current-public namespace
already present yields UNEXPECTED_EXISTING_PUBLIC_PROJECTION without removal.
Production and association/inventory natural cycles remain independent of source sync.

## Tests and gate limits

Pure/public/privacy/intersection/history/determinism tests use varied synthetic
counts. Injected Windows reader tests exercise actual reader control flow and
native flag/ACL methods, exact metadata checks, transaction limits, deadline,
replacement, complete reads, busy/no retry and descriptor/lock cleanup.
Actual engine main tests use temporary state and fake MQTT; assert pre-discovery
stripping, source-field stripping, success/omission/import/read/public/internal
failure, local files, unchanged non-device outputs/events/compatibility/topics/
connections/status and MQTT failure behavior. Source validator tests inject contexts
only; its native production path is not executed on Windows.
Linux/POSIX-only reader tests use controlled temporary directories and real locks,
symlinks/hardlinks/permissions/dirty namespaces. They are skipped on Windows and
remain pending actual later PI3 execution. Windows success is not actual POSIX proof.

Initial implementation run: 100 total, 98 passed, 2 POSIX skips, no failure/error.
Initial validator run: 9 total, 8 passed, 1 failure, 0 errors/skips. The new AST
check mistook string replacement of a schema filename for filesystem replacement;
corrected that test only. Additional cleanup/binding/ACL tests then passed.
First complete PE-4 run: 1655 total, 1633 passed, 18 skipped, 4 failures, 0 errors.
The failures were stale current-tree identity assertions in adapter implementation
preparation, independent acceptance preparation, credential provisioning and its
closure tests. They still bind every frozen predecessor byte; only the governed
inventory engine / DATA_MODEL current identities now bind the implementation record.
No historical record, security rule, producer or timing threshold was changed.
The harness stopped before full discovery. Final native Windows rerun:

| Suite | Total | Passed | Skipped | Failures | Errors |
| --- | ---: | ---: | ---: | ---: | ---: |
| Focused implementation | 108 | 106 | 2 | 0 | 0 |
| Source validator | 9 | 9 | 0 | 0 | 0 |
| Expanded targeted compatibility | 597 | 595 | 2 | 0 | 0 |
| Complete PE-4 | 1655 | 1637 | 18 | 0 | 0 |
| Full repository | 2380 | 2331 | 49 | 0 | 0 |

No timing-sensitive flake occurred. No threshold or assertion was suppressed.
Full-regression production-label stdout belongs to mocked fixtures, not production
execution. Actual Linux/POSIX tests remain skipped and PI3 validation pending.
Final metadata-only evidence refresh requires focused governance checks before commit.
An evidence-write command initially failed in PowerShell parsing before execution;
corrected quoting, with no repository changes from that rejected command.

Reproduction: from the HIOC repository, supply the Python block below on standard
input to the bundled native Windows interpreter with -B -:
C:\Users\JorgeAzofeifaCastill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe.
The harness excludes Bash/sh from PATH, clears HIOC_TEST_SHELL, disables bytecode
and stops on any failed suite.

```python
import os,sys,shutil,unittest
from pathlib import Path
win=Path(os.environ['SystemRoot'])
os.environ['PATH']=os.pathsep.join(map(str,[win/'System32',win,win/'System32/WindowsPowerShell/v1.0',Path(os.environ['ProgramFiles'])/'Git/cmd',Path(sys.executable).parent]))
os.environ.pop('HIOC_TEST_SHELL',None)
assert not shutil.which('bash') and not shutil.which('sh') and shutil.which('git')
sys.path[:0]=['tests','pi4/lib']
targeted=['test_pe4_ha_association_public_projection_preparation','test_pe4_0c_association_contract','test_pe4_0c1_association_lifecycle','test_pe4_ha_association_adapter','test_pe4_ha_association_scheduler_deployment_closure','test_inventory','test_inventory_presentation','test_mqtt_runtime_validation','test_mqtt_dashboard_health','test_release','test_hostname_enrichment','test_pe4_ha_association_independent_production_acceptance_closure','test_compatibility_master_plan_governance','test_pe4_ha_association_implementation_preparation','test_pe4_ha_association_independent_production_acceptance_preparation','test_pe4_ha_runtime_credential_provisioning','test_pe4_ha_runtime_credential_provisioning_closure']
for label,names in [('FOCUSED',['test_pe4_ha_association_public_projection']),('VALIDATOR',['test_pe4_ha_public_projection_source_validate']),('TARGETED',targeted),('PE4',None),('FULL',None)]:
 suite=unittest.defaultTestLoader.loadTestsFromNames(names) if names else unittest.defaultTestLoader.discover('tests',pattern='test_pe4*.py' if label=='PE4' else 'test*.py')
 r=unittest.TextTestRunner(verbosity=0).run(suite)
 print(label,'TOTAL=',r.testsRun,'PASS=',r.testsRun-len(r.skipped)-len(r.failures)-len(r.errors),'SKIP=',len(r.skipped),'FAIL=',len(r.failures),'ERROR=',len(r.errors),flush=True)
 if not r.wasSuccessful():raise SystemExit(1)
```

## Immediate handoff

PI3 SOURCE SYNCHRONIZATION TO THE SOURCE-IMPLEMENTATION COMMIT ONLY, then STOP AND
INDEPENDENT SOURCE REVIEW. Read-only PI3 POSIX source validation is a separate
future authorization; no sync command executes it. Deployment and production
projection remain NOT STARTED. No deviation from the frozen architecture: explicit
2-second copy checkpoints operationalize its finite deadline, and verified-byte
module execution operationalizes its before-import identity check without refactoring.
