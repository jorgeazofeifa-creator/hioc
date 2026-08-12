# HIOC Python Runtime Compatibility

## Authority and scope

This document is the authoritative compatibility policy for every Python
program in HIOC: production runtime code, repository tools, release and
validation tooling, tests, and Windows operator procedures. It governs runtime
family, language floor, tested evidence, supported operational lines, patch
policy, prerequisite validation, and support promotion. Project status remains
owned by [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Compatibility model

HIOC uses Model D: language compatibility, tested evidence, supported runtime,
and operational recommendation are separate claims.

### Language floor

The language floor is **CPython 3.10**. A repository-wide audit found PEP 604
union syntax such as `X | None` in production modules, including modules where
annotations are evaluated normally. Python 3.9 cannot parse that syntax. The
audit found no syntax or standard-library API that raises the current floor
above 3.10.

The floor means only that the current source requires Python 3.10 or newer to
parse and execute. It does not make every Python version at or above 3.10
supported.

### Implementation family

The governed implementation is **CPython**. HIOC does not claim compatibility
with PyPy, GraalPy, IronPython, Jython, or another implementation unless that
implementation is separately tested and governed.

### Tested and supported definitions

- **TESTED** means the complete repository suite passed using an exact recorded
  interpreter version. It is evidence only for that version and environment.
- **SUPPORTED** means an operational major/minor line has an approved repository
  support record after its exact patch, execution probe, complete suite, and
  applicable focused tests passed.
- **PROPOSED / VALIDATION PENDING** means the line is selected for validation but
  is not yet permitted to gate production work.

## Current status

| Runtime | Status |
| --- | --- |
| CPython 3.10 | LANGUAGE-COMPATIBLE FLOOR; NOT CLAIMED TESTED/SUPPORTED |
| CPython 3.11 | NOT YET REPOSITORY-VALIDATED AS A GOVERNED LINE |
| CPython 3.12.13 | TESTED — FULL SUITE PASS |
| CPython 3.13.x | PROPOSED WINDOWS OPERATOR LINE — VALIDATION PENDING |
| CPython 3.14.7 | PRESENT FROM OPERATOR-DIAGNOSTIC SIDE EFFECT; NOT HIOC-SUPPORTED |
| Production Python | EXACT VERSION UNVERIFIED |

The machine-readable support state is
`governance/python-runtime-support.json`. It is explicit repository state, not
chat state. Its Windows status remains `validation_pending`; therefore PE-3
Production Action 1 remains blocked even if a Python 3.13 interpreter appears.
The official Python Install Manager is present on the operator workstation.
CPython 3.14.7 is also present because an informal `py --help` diagnostic
triggered the manager's default-runtime automatic installation. Its presence
does not satisfy, block, or change the governed 3.13.x contract.

## Windows operator runtime

The proposed Windows operational line is official CPython 3.13.x. Patch
versions may float within the line. It becomes **SUPPORTED — WINDOWS OPERATOR**
only after a separate governed checkpoint:

1. installs an official CPython 3.13 runtime;
2. records its exact patch version;
3. verifies `py -3.13` by actual execution and implementation/version probe;
4. runs the complete repository suite with that interpreter;
5. runs the Action 1-focused tests and prerequisite probes; and
6. commits a support-state promotion setting `windows_operator.status` to
   `supported` and `validated_patch` to the exact passing `3.13.x` version.

The installation and compatibility action is the repository-controlled script
`tools/hioc-python313-validate.ps1`. Never reproduce its source through chat.
Its governed identities are:

```text
PYTHON313_CHECKPOINT_SHA256=a26fea5033d2bb499a69c0c604f5989c06243275ceb5b64c2bb54cc004faa938
PYTHON313_CHECKPOINT_GIT_BLOB=f43b75573d7f58c1fbbae35a9d0c298687f88169
```

After its commit is approved and pushed, prepare only this short invocation:

```powershell
$Repo = Read-Host 'Enter the authoritative HIOC repository path'
$GovernanceCommit = Read-Host 'Enter the approved full 40-hex post-push governance commit'
$CheckpointScript = Join-Path $Repo 'tools/hioc-python313-validate.ps1'
& $CheckpointScript -Repo $Repo -GovernanceCommit $GovernanceCommit
```

The script verifies its own Git identity and the synchronized clean repository,
requires support state `validation_pending`, installs only through the official
WinGet Python Install Manager package, and uses the unambiguous `pymanager`
command for scripted list/install operations. It disables automatic runtime
installation before any runtime launcher can execute, explicitly runs
`pymanager install 3.13`, resolves the exact managed 3.13 interpreter through
`pymanager list --one --format=exe --only-managed 3.13`, and invokes that real
interpreter for the governed execution probe and validation matrix. It emits sanitized evidence and
does not edit support state. Promotion is a separate repository checkpoint
after evidence review.

The first governed checkpoint attempt stopped at `PYTHON_INSTALLATION` with
`PYTHON_CHECKPOINT_UNEXPECTED_ERROR`. Forensic review confirmed a **PYTHON
CHECKPOINT NATIVE STDERR HANDLING DEFECT**: Windows PowerShell 5.1 can promote
informational native stderr to `NativeCommandError` / `RemoteException` under
`$ErrorActionPreference = 'Stop'` before `$LASTEXITCODE` is evaluated. The
checkpoint now captures native stdout, stderr, and exit status through one
PowerShell 5.1-compatible process helper. Stderr with exit zero is success;
nonzero exit remains failure; routine output is not exposed.

The corrected checkpoint then progressed through explicit installation and
stopped at `PYTHON_PROBE` with `PYTHON_CHECKPOINT_UNEXPECTED_ERROR`. This
confirmed the remaining **PYTHON CHECKPOINT NATIVE STDERR HANDLING DEFECT —
RUNTIME INVOCATION PATH**: the probe, test runner, and compilation path still
used direct native invocation under PowerShell's stop-on-error policy. This is
not CPython compatibility, HIOC test, manufacturer, version-rejection, PE-3, or
production failure. CPython 3.13.x may already be installed, but its exact patch
and compatibility are not established until governed evidence passes.

Every native executable in the checkpoint now uses one process wrapper with a
deterministically quoted argument list, space-safe paths, bounded stdout/stderr
capture, and actual native exit status. This includes Git, WinGet, `pymanager`,
`py -3.13`, every test stage, and `compileall`. Informational stderr with exit
zero succeeds; nonzero exit fails at the bounded current stage. No routine
evidence prints executable paths or captured command output.

Before installation, `pymanager list --one --format=json --only-managed 3.13`
provides the manager's deterministic authoritative selection. One valid entry
is reused without reinstalling; none triggers the sole explicit
`pymanager install 3.13`; malformed JSON or a non-authoritative multiple result
fails closed. CPython 3.14 remains irrelevant to selection.

The operator's later `pymanager install --dry-run 3.13` inspection was
non-mutating and resolved CPython 3.13.15 as the current candidate. This patch
is observed evidence, not a permanent pin: the governed line remains 3.13.x and
the exact installed patch is recorded only after successful validation.

The approved installation mechanism is the current official Python Install
Manager supplied by the CPython project. Installation through the official
Windows/WinGet mechanism is acceptable. Microsoft WindowsApps placeholders are
not proof of a Python installation. `Get-Command`, `where`, or name resolution
alone is insufficient: the runtime must execute and report the governed CPython
implementation and version. Installation is outside this checkpoint.

External lifecycle and installer authority:

- [CPython supported-version status](https://devguide.python.org/versions/)
- [Official Python on Windows and Python Install Manager](https://docs.python.org/3/using/windows.html)
- [Official Python Windows downloads](https://www.python.org/downloads/windows/)

Action 1 disables Python Install Manager automatic installation while probing.
Its resolver order is `py -3.13`, `python3`, then `python`; either fallback is
accepted only when it executes as CPython 3.13. A usable incompatible runtime is
`PYTHON_VERSION_UNSUPPORTED`; no usable runtime is `PYTHON3_NOT_FOUND`.

## Production and Raspberry Pi runtime

Production uses the distribution-managed CPython `python3`. Do not replace the
system interpreter merely to match Windows. The exact production major/minor
must be discovered and validated independently during governed PI validation.
Until then, **PRODUCTION PYTHON VERSION — UNVERIFIED**. No production support
claim follows from Windows or repository test evidence.

## Patch policy

HIOC governs operational major/minor lines. Patch releases may float within an
approved line and are not permanently pinned unless a future regression
requires it. Every newly installed patch must pass the bounded execution,
implementation, version, platform, and applicable repository validation for its
environment before it is relied upon.

## Operator prerequisite governance

The workstation used to operate HIOC is part of the controlled operational
environment for prerequisites, reproducibility, and validation. It is not
production infrastructure, but its tooling may gate production procedures.

Every operator prerequisite must establish:

- tool identity;
- implementation or runtime family where relevant;
- supported version or governed operational line;
- actual execution and version probes;
- platform compatibility;
- alias-versus-runtime distinction;
- sanitized precondition failure; and
- prerequisite-failure classification distinct from product failure.

A command merely resolving by name does not satisfy a prerequisite.

Diagnostic commands must themselves be assessed for side effects before
execution. A command described informally as a "probe" is not automatically
read-only. External tool-manager diagnostics must use documented `list`,
`inspect`, `version`, or `dry-run` forms known not to install or mutate state.

On Windows PowerShell 5.1, validation-critical native executables must be
evaluated by native exit code through a governed process-execution wrapper.
Informational stderr alone never determines success or failure. Operator tools
must not mix wrapped management calls with direct runtime or validation calls.

Cross-platform regression tests must distinguish a missing optional platform
tool from a failed assertion. Tool-dependent tests skip explicitly and visibly
only when the prerequisite is unavailable; platform-neutral assertions remain
active, and the complete original semantics must run wherever the tool exists.

## Repository-controlled operator programs

Validation-critical or production-capable multi-line operator programs should
be stored and versioned in Git whenever practical. Operator guidance invokes
the governed artifact instead of reproducing its source through chat. This
preserves source integrity, Git identity, reproducibility, reviewability, and
testability while avoiding escaping and copy corruption.

## PE-3.3 prerequisite chronology

The original PE-3 Production Action 1 was delivered as PowerShell source through
chat. Delivery altered literal syntax, including escaped underscores and
PowerShell/Python expressions. Those attempts are **ACTION 1 DELIVERY PATH
DEFECTS**, not Python, manufacturer, dataset, repository, or production
failures.

HIOC moved the program to `tools/hioc-pe3-action1.ps1`. Repository-controlled
execution eliminated chat/copy transport as a variable. The governed script
then genuinely returned `FAILURE_STAGE=PYTHON_RESOLUTION`. Read-only diagnostics
found `py` absent; `python3` and `python` resolved only to nonfunctional
WindowsApps aliases, reported Python absent, and returned 9009; a bounded search
found no real installation. This is **ACTION1_PREREQUISITE_MISSING — PYTHON3**.

Repository review then found no governed Python minimum or supported-version
contract. The resulting audit established the 3.10 language floor, recorded
3.12.13 full-suite evidence, proposed 3.13.x for Windows pending validation, and
kept production runtime validation independent. These are distinct findings.

The official manager was then installed, but the first governed installation
checkpoint stopped at `PYTHON_INSTALLATION`. A subsequent diagnostic invoked
`py --help` before automatic installation was disabled; with no managed runtime
present, the manager installed its default CPython 3.14.7. This is
`PYTHON_OPERATOR_DIAGNOSTIC_SIDE_EFFECT — UNINTENDED_DEFAULT_RUNTIME_INSTALL`,
not support promotion, 3.13 validation, PE-3 failure, or production failure.
The runtime remains present pending a separate cleanup decision and is never
selected for HIOC. A safe manager dry run subsequently identified CPython
3.13.15 as the current 3.13 candidate. No 3.13 installation or validation has
yet been established by accepted evidence.

The corrected checkpoint later passed its explicit installation stage and then
failed at `PYTHON_PROBE`. That progression means a 3.13 runtime may now exist,
but inference cannot establish its patch or compatibility. Forensic review
traced the stop to the remaining direct runtime invocation path, extending the
same native-stderr defect already found in manager calls. The hardened retry
must safely inspect and reuse a managed 3.13 entry before considering install,
then establish its exact patch only through the wrapped `py -3.13` probe.

The next governed execution reached `FULL_REGRESSION`. A direct verbose rerun
proved CPython 3.13 launched and ran 504 tests; only three errors occurred, all
in `test_network_probe_governance.py`, where Bash-specific scripts were invoked
through an unresolved fallback command and raised Windows `FileNotFoundError`
(`WinError 2`). This is **CROSS-PLATFORM TEST PREREQUISITE CONTRACT DEFECT —
MISSING BASH REPORTED AS ERROR**, not Python 3.13 incompatibility or an HIOC,
manufacturer, PE-3, or production failure.

Those three tests exercise Bash-only syntax and behavior. They now follow the
repository's existing per-test prerequisite contract: each visibly skips with
`Bash is required` when neither the governed `HIOC_TEST_SHELL` nor `bash`/`sh`
is resolvable. The module's three platform-neutral governance tests still run.
When Bash is available, all six original assertions execute unchanged. The
full regression continues to fail on real failures/errors, reports actual test
and skip counts, and permits explicit tool/platform skips without hard-coded
counts.

After that correction, the governed checkpoint again reported
`FULL_REGRESSION_FAILED`. An immediate direct execution on the same workstation,
repository, and governed CPython 3.13 runtime ran 506 tests in 14.889 seconds and
returned `OK (skipped=13)` with native exit code 0. This is authoritative proof
that the full regression passed and that the checkpoint result was false.

Forensic review found **CHECKPOINT FULL-REGRESSION RESULT-CLASSIFICATION DEFECT —
NON-AUTHORITATIVE SUMMARY PARSE USED AS ACCEPTANCE GATE**. The wrapper correctly
derived `Passed` from the native process exit code, but the stage separately
required a parsed `Ran` count greater than zero. Its bounded capture retained
the beginning of each stream, while `unittest` writes its result summary at the
end. A successful run whose summary was outside the retained window therefore
produced `Passed=True`, `Ran=0`, and the false failure. `OK (skipped=13)` was not
rejected as a skip-count mismatch; no test or skip count was governed as an
acceptance threshold.

The corrected checkpoint preserves the end of bounded native output and bases
test-stage acceptance only on the actual native exit status. Parsed test and
skip counts remain sanitized reporting fields only. Genuine nonzero exits still
fail closed, and no test/skip total is hard-coded. Support remains
`validation_pending` with `validated_patch: null` until a fresh execution of the
corrected governed checkpoint passes and a separate commit promotes support.

The corrected governed checkpoint nevertheless returned
`FULL_REGRESSION_FAILED` again. Direct `py -3.13` execution then passed 508 tests
with 13 skips and exit code 0, including an equivalent run with the checkpoint's
temporary `PYTHONPYCACHEPREFIX`. This rules out CPython 3.13 compatibility, the
repository suite, Bash prerequisite handling, PyYAML skips, the pycache prefix,
and short-invocation delivery as explanations. The remaining unreplicated
difference is the Windows PowerShell 5.1 `ProcessStartInfo` execution/capture
path.

Codex's repository process cannot resolve the operator's `py` launcher, so an
exact same-launcher reproduction is not possible in that environment. The
repository-controlled diagnostic `tools/hioc-python313-process-diagnostic.ps1`
must be committed and pushed before one operator execution. It compares direct
PowerShell and current `ProcessStartInfo` semantics using the same launcher,
arguments, environment, working directory, and test suite, and emits only exit
codes, lengths, task/completion states, parsed counts, and equality flags.

```text
PYTHON313_PROCESS_DIAGNOSTIC_SHA256=e77e1c1f948a7a62dac7d3eb971e181e3fd2baf65dd08f45980554adcbf397d3
PYTHON313_PROCESS_DIAGNOSTIC_GIT_BLOB=d5ad172e5f0d98c76ad68d357424716c859331d4
```

Future preparation must provide only a short invocation of that checked-in
file with `-Repo` and `-GovernanceCommit`; its source must not be transported
through chat. Until its governed evidence establishes the exact mechanism, no
further speculative checkpoint change or support promotion is permitted.

A validation wrapper must itself be production-grade tested. Any wrapper result
that differs from the native process result is a validator defect and never
product incompatibility. Diagnostic equivalence requires the same executable,
arguments, environment, working directory, and execution wrapper before a
failure is attributed to the product.

The governed diagnostic completed and proved execution equivalence failed. Its
direct full regression exited 0, ran 516 tests with 13 skips, and produced a
valid summary. `ProcessStartInfo` launched the same resolved `py` App Execution
Alias, both redirected stream tasks completed, but the process exited 1 with no
stdout or unittest summary and 1454 bytes of stderr. The minimal and argv probes
also diverged. The earlier top-level `RESULT=PASS` meant only that the diagnostic
completed; it did not mean equivalence passed. The corrected contract emits
`DIAGNOSTIC_EXECUTION=PASS` separately from `EQUIVALENCE_RESULT=PASS|FAIL`.

This establishes **WINDOWS APP EXECUTION ALIAS / PROCESSSTARTINFO RUNTIME-LAUNCH
DIVERGENCE**. It does not establish Python incompatibility or a regression
failure. The raw stderr was not exposed and no evidence-supported narrow error
signature is yet available, so no speculative stderr enum is frozen.

The official Python documentation says `pymanager exec` is equivalent to `py`,
and also provides machine-oriented `list` formats including `exe`. Three models
were evaluated: Model A retains the disproven Alias path; Model B uses the
manager's `exec` layer and may automatically install unless separately disabled;
Model C resolves the selected managed runtime with
`pymanager list --one --format=exe --only-managed 3.13` and invokes the exact
interpreter. Model C is adopted because it has the fewest launcher layers,
cannot select the installed 3.14 runtime, avoids default selection and automatic
installation, and retains the existing tested native wrapper.

Windows App Execution Alias commands must not automatically be treated as
ordinary executable paths for `ProcessStartInfo` automation. Their behavior
must be validated for the exact invocation model, or an underlying governed
runtime must be resolved through an officially supported scripted interface.
A diagnostic's execution success is distinct from the state it diagnoses.

## Future validation matrix

Continuous validation should eventually run the complete suite on every
supported operational line and the language-floor line, on relevant Windows and
Linux architectures. Until such a matrix exists, support claims remain limited
to explicitly recorded evidence and approved support-state promotions.
