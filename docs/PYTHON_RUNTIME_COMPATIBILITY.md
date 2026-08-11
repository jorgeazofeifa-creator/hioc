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
| CPython 3.14.x | NOT CURRENTLY GOVERNED |
| Production Python | EXACT VERSION UNVERIFIED |

The machine-readable support state is
`governance/python-runtime-support.json`. It is explicit repository state, not
chat state. Its Windows status remains `validation_pending`; therefore PE-3
Production Action 1 remains blocked even if a Python 3.13 interpreter appears.

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

## Future validation matrix

Continuous validation should eventually run the complete suite on every
supported operational line and the language-floor line, on relevant Windows and
Linux architectures. Until such a matrix exists, support claims remain limited
to explicitly recorded evidence and approved support-state promotions.
