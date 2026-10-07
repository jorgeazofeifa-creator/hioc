# Independent Production Acceptance Capture Correction

Capture Correction PASS/CLOSED; Independent Production Acceptance NOT CLOSED.
Attempt 1 FAIL / DURABLE CAPTURE. Its read-only inspection portion returned PASS/rc0,
but validation.json and manifest.json were NOT PUBLISHED. These are
OPERATOR_SUPPLIED_WINDOWS_AND_PRODUCTION_EXECUTION_EVIDENCE, not Codex PI3 observations.
Remote sanitized output length was reported as 560 bytes. SSH_STDERR_DISCARDED=False and
remote_stderr_present=false are separately supplied fields, not equivalent claims.
The failed run directory is historical, untouched, never reused. Original stdout is
UNAVAILABLE_FOR_DURABLE_REVALIDATION; no inferred report or regenerated evidence is created.

## Proven local serializer defect

Synthetic closed-schema reports only: Python sorted compact ASCII JSON plus LF is 560 bytes.
Windows PowerShell 5.1.26100.9444 ConvertTo-Json -Compress produces 565 bytes. The first
difference is zero-based byte 550 (one-based 551): Python & (0x26), PowerShell backslash
(0x5c) beginning \u0026, in TARGET=PI3 NUT&PIHOLE. Windows PowerShell's HTML escaping
causes canonical byte mismatch despite equivalent parsed JSON. Ordering, types and LF agree
in this reproduction. PowerShell 7.6.5 produced identical bytes. No historical lost bytes
were used; reproducing the defect cannot revalidate or recover Attempt 1 stdout.

## Workstation correction only

The new tools/hioc-pe4-ha-association-acceptance-capture.py is an OFFLINE workstation helper,
not a production inspection engine. It performs no SSH, HA, credential or production access.
It consumes ORIGINAL received bytes on binary stdin, a remote return code, exact reviewed
correction source commit and NEW unique run ID. Explicit absolute local CPython >=3.12,
-I -B, no ambient PYTHONPATH; source must be clean main/origin at the exact correction commit,
direct parent 16b7dd4 and exact correction subject; helper bytes must match Git.

It validates size 1..4096, ASCII, LF/no CR, strict JSON/no duplicate keys/no nonfinite values,
exact fields, bounded gates/stages, source/target/mode, activity false and mandatory limitation.
PASS requires rc0/all gates PASS/stage NONE; FAIL requires rc1/non-NONE stage.
Python canonical(parsed)==ORIGINAL bytes is mandatory. Canonicalization never substitutes
received bytes. PowerShell serialization is not a canonical acceptance authority.

Future integration: retain raw SSH stdout as byte[]; discard SSH stderr; invoke this local
helper as a binary-stdin process and pass the measured remote return code. Never pipe through
text decoding, ConvertTo-Json or PowerShell native string piping. Read and validate the bounded
bytes BEFORE publication. A nonzero helper result remains capture FAIL and requires STOP.
No transport command or Acceptance Attempt 2 is authorized here.

Governed Windows evidence root stays under operator LOCALAPPDATA/HIOC/evidence/pe4/
independent-acceptance/<correction-commit>/<NEW-run-id>. Parent must be independently prepared
and validated, protected DACL owned by operator, only operator/SYSTEM/Administrators full control,
no reparse points. Helper never creates parent hierarchy or touches old run directories.
Only its newly created exclusive run receives its protected ACL. validation.json is written
from original bytes using exclusive creation, fsync and reopen comparison. manifest.json,
canonical schema_version/source_commit/validation_sha256/validation_bytes, is published LAST.
Flush and reopen both files/directories; unsupported Windows directory durability fails closed.
Windows filesystem/ACL/directory-flush compatibility MUST be separately tested with synthetic
workstation data before any Attempt 2 authorization; memory-only synthetic publisher tests do
not claim native evidence durability. No retry, overwrite, repair or evidence recreation.
Original preparation privacy allowlist and durable retention rule remain mandatory.

## Governance and future attempt

NO AUTOMATIC RETRY is preserved. A fresh read-only attempt can be prepared for independent review
and explicit separate authorization because the original rule forbids automatic retries; it does
not permanently prohibit reviewed read-only inspection. Attempt 2 is NOT STARTED / PREPARED FOR
SEPARATE AUTHORIZATION and NOT AUTHORIZED. It uses a new directory and the same read-only
inspection functions. No second adapter invocation or reconciliation execution is permitted.

Original ephemeral evidence still absent, revalidation UNAVAILABLE, limitation RECORDED,
disappearance cause UNKNOWN; no execution-time comparison or historical evidence recreated.
No FULL_ORIGINAL_ARTIFACT_REVALIDATION or ZERO_EVIDENCE_GAPS claim. Scheduler NOT STARTED,
projection DEFERRED, PE-4 NOT COMPLETE, Phase 7A ACTIVE, rollback NOT PERFORMED.
Next action: source synchronization to correction commit ONLY; STOP and independent review.
Codex performed repository work and synthetic local tests only.
