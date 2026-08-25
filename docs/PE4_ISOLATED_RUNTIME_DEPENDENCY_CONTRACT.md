# PE-4 Isolated Runtime and Dependency Contract

## Status and authority

This repository-only checkpoint governs the future PI3 runtime for the
PE-4.0B.2a Home Assistant capability client. It does not install, deploy, or
execute anything. PE-4.0B.2a remains **NOT STARTED**.

```text
PI3_PYTHON_POLICY=SATISFIES_EXISTING_HIOC_POLICY
PI3_PYTHON_RUNTIME=CPYTHON_3_11_2
PYTHON_VERSION_CHANGE_REQUIRED=FALSE
DEPENDENCY_ARCHITECTURE=CASE_A_ISOLATED_RUNTIME
READINESS=READY_FOR_PE4_0B2A_ISOLATED_RUNTIME_GOVERNANCE_COMMIT_REVIEW
```

The existing Python policy remains authoritative: CPython 3.10 is the language
floor and production uses its independently validated distribution-managed
`python3`. The observed PI3 CPython 3.11.2 runtime satisfies that policy. This
checkpoint does not replace, upgrade, or otherwise modify the system Python.

## Frozen dependency artifact

The sole third-party runtime dependency is `websockets==16.1.1`. Its official
PyPI metadata declares Python `>=3.10`, includes Python 3.11 support, and lists
no required distributions. Consequently the governed transitive dependency set
is empty.

```text
PROJECT=websockets
VERSION=16.1.1
FILENAME=websockets-16.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl
SIZE_BYTES=188095
SHA256=86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01
PYTHON_TAG=cp311
ABI_TAG=cp311
PLATFORM_TAGS=manylinux2014_aarch64,manylinux_2_17_aarch64,manylinux_2_28_aarch64
TRANSITIVE_DEPENDENCIES=NONE
```

The wheel matches the observed CPython 3.11 AArch64 Linux SOABI. The exact
filename, byte count, digest, and package/version must all match before it can
enter a later deployment. A differently named file, sdist, universal wheel,
different version, different digest, or additional dependency fails closed.
The artifact isn't committed to Git. It must be retained in a governed durable
off-device artifact cache or backup; a PI3 transfer location is temporary and
invocation-owned.

`requirements-pe4.lock` is the machine-readable project/version/hash lock.
Installation must be offline and hash-enforced with the isolated interpreter:

```text
python -m pip install --no-index --no-deps --require-hashes --only-binary=:all: --find-links <private-wheel-directory> -r requirements-pe4.lock
```

`<private-wheel-directory>` is a future deployment-tool-owned private input,
not an operator-selected reusable directory. `--no-deps` is permitted only
because official metadata records no required distributions. No live package
index, resolver drift, dependency upgrade, vendoring, or unbounded pip upgrade
is permitted. The isolated pip version and its required option capabilities
must be recorded and validated before installation; `ensurepip` may bootstrap
pip without network access but isn't proof of the dependency installation.

## PI3 filesystem and interpreter contract

The release-managed runtime layout is:

```text
RUNTIME_ROOT=/home/jazofv1/hioc/runtime/pe4
ENVIRONMENT_ROOT=/home/jazofv1/hioc/runtime/pe4/environments
VERSIONED_ENVIRONMENT=/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1
ACTIVE_POINTER=/home/jazofv1/hioc/runtime/pe4/active
ACTIVE_INTERPRETER=/home/jazofv1/hioc/runtime/pe4/active/bin/python
CLIENT=/home/jazofv1/hioc/tools/hioc-pe4-ha-auth-capability.py
OWNER_GROUP=jazofv1:jazofv1
```

Runtime root, environment root, and versioned environment are mode `0750`;
the deployed client is mode `0700`; a private artifact staging directory is
mode `0700` and its wheel is `0600`. The repository lock is ordinary reviewed
release content (`0644`). No governed path may be group- or world-writable.
Symlinks are rejected throughout except for the strictly managed active pointer.

The environment is created with `/usr/bin/python3 -m venv` without
`--system-site-packages`. It is validated as CPython 3.11.2 with the expected
Linux AArch64/SOABI, isolated `sys.prefix`, no system-site inheritance, the
exact installed dependency version, and the client-required API surface.
The client and environment form one compatibility unit and the client is
invoked only with `ACTIVE_INTERPRETER`, never an ambient `python` or directly
from release source.

The active pointer target is not caller supplied. A future repository tool must
validate a basename-only target under `ENVIRONMENT_ROOT`, prove that target is
complete and non-symlinked, and replace the pointer atomically. The previously
active immutable environment is preserved for immediate pointer rollback.
Symlink mode isn't treated as an access-control boundary; directory ownership
and permissions are authoritative.

## Lifecycle, rollback, and evidence

The isolated environment is reproducible release content, not persistent
application state. Future backup/restore governance must preserve the lock,
artifact identity, durable off-device wheel, deployment tooling, and prior
active environment needed for bounded rollback; it must not treat arbitrary
environment bytes as irreplaceable state. Ordinary release backup exclusions
may omit environment bytes only after that correction is separately reviewed.

A later deployment must create a new versioned environment, validate it fully,
deploy the identity-checked client, atomically activate it, and rerun the full
credential-free runtime preflight through the absolute active interpreter.
Failure before activation leaves the current pointer unchanged. Failure after
activation restores only the preserved prior pointer when the governed rollback
contract says to do so. It never changes system Python or production data.

The independent credential-free PI3-to-PI5 route proof should precede runtime
deployment to preserve fault isolation. Neither proof authorizes credentials,
Home Assistant access, client execution, PE-4.0B.2b, or PE-4.0C.

The executable lifecycle, separate A-G authorization boundaries, evidence,
cleanup, backup, and rollback rules are governed by
`PE4_ISOLATED_RUNTIME_LIFECYCLE.md`. Implementation does not authorize use.
Action A's Windows cache, evidence, DACL, reparse, deadline, partial-success,
and bounded-CLI semantics are governed there; it never uses `/tmp`.
The production ACL correction retains the same security invariant while
removing PowerShell ACL-cmdlet dependence: existing descriptors are hardened
and persisted through Windows .NET file/directory APIs. The first attempt did
not acquire the wheel. The corrected retry established Action A production
PASS and the durable cache. Action B derives that fixed cache internally,
validates its DACL/reparse boundary and exact artifact/lock identities, uses
bounded system OpenSSH, records partial states in result-last evidence,
preserves its private PI3 directory, and stops.
