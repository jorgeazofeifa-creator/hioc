# PE-6.4 independent acceptance workflow

Status: repository preparation candidate; not PE-6.4 closure, execution authority,
publication authority, or a retrospective permission. PE-6.4 remains OPEN. The
original second-acceptance receipt remains unchanged INSUFFICIENT_EVIDENCE.

## Authority and selected boundary

The [Master Plan](HIOC_MASTER_PLAN.md#permanent-operational-governance-no-assumptions)
requires unknown material facts to remain UNKNOWN and operator observations to
remain OPERATOR_SUPPLIED. Its Repository and Deployment Governance and Operations
Acceptance Standard preserve the source/runtime boundary and durable reporting.
The [PE-6.4 contract](PE6_CLASSIFICATION_CONTRACT_DESIGN.md#pe-64--bounded-execution-and-concise-independent-production-acceptance)
requires separately authorized operator-only offline execution once, a sanitized
schema/count/hash/explanation/protected-invariant receipt, THEN independent
repository acceptance. No recurring activation is authorized.

This workflow implements that existing review boundary, not another lifecycle
checkpoint or a replacement protected-state gate. It does not require that a
later independent judgment reproduce the helper's internal permission calculation.
Independent acceptance must establish the protected invariants and exact permitted
changes from evidence; it cannot merely accept an explanation for a failed gate.

| Boundary | Required facts and responsibilities |
| --- | --- |
| Production execution | Approved release/dependency identities, secure Reader, one authorized evaluation, eight protected categories, independent primary/inspection outcomes, complete comparison, sanitized bounded receipt. Existing instrument is unchanged. |
| Sanitized receipt | Execution identity, functional positive evidence, origins, outcome stages, capture times/digests/completeness, complete change count and untruncated differences, identifiers, changed fields, original hashes and explicit NOT_CAPTURED fields. A digest binds supplied evidence; it does not disclose or independently prove its preimage. |
| Independent repository review | Preserve and bind the exact original receipt; verify numerical bindings, source authority, complete scope and functional/protected outcomes; examine separate native PE-5 validation and actual writer authorization; issue a separate reasoned judgment with limitations. |
| External authorization | Existing accepted PE-5 activation scope and evidence of its continued applicability; independent acceptance of the responsible writer and exact three changes. A string, boolean, matching schedule, filename or claimed writer is not authorization. |

## Options considered

- A, sufficient sanitized evidence: selected with D. Use complete differences plus
  separately supplied native validation and independently reviewed authority.
  Full private captures are unnecessary when these establish every material fact.
  If a particular receipt omits a material fact not otherwise established, STOP;
  this workflow cannot make an incomplete receipt sufficient.
- B, in-memory interactive adjudication: not required by the governing contract.
  It would add an approval transport, identity verification, waits/timeouts and
  operational failure modes. No interactive service, archive or background process
  is introduced. Existing capture objects remain private and ephemeral.
- C, pre-authorized exact operations: existing PE-5 activation establishes the
  producer's allowed operations, not blanket approval of every mutation. Apply
  that authority only after exact observed effects and writer evidence are reviewed.
  No new producer allowlist or future-mutation permission is created.
- D, separate independent repository acceptance: selected. The reviewer evaluates
  the evidence and external authority after execution and records its own judgment.
  This is distinct from helper replay and from alteration of the historical receipt.

No code change is necessary. The existing helper and instrument remain unchanged.
In particular, ReviewedPermission still requires real captures for build_report();
no receipt-to-Capture conversion, invented fingerprints or purported helper replay
is permitted. A later review judgment is not a ReviewedPermission supplied to a
past execution and must never be presented as such.

## Finite review procedure

1. Identify the original receipt by SHA-256 of its exact supplied JSON bytes,
   excluding surrounding prose/Markdown fences, and preserve those bytes unchanged.
   If only a parsed representation survives, label any canonical representation's
   digest as canonical JSON, not the original byte digest. Record the instrument,
   helper and source identities from that receipt and their accepted authority.
   Repository identity is an IMMUTABLE_REPOSITORY_FACT; production identity and
   observations retain their supplied evidence class. A new helper release does
   not establish which helper executed historically.
2. Check primary functional PASS, positive classification evidence, one invocation,
   both origin checks, and successful independent protected inspections. Cross-check
   outer and nested primary/inspection outcomes. Known primary or protected FAIL
   blocks acceptance regardless of producer permissions. Missing positive evidence
   is insufficient, not a functional PASS. Unstable/incomplete captures, unordered
   intervals, truncation, omitted differences or contradictory counts block acceptance.
3. Require all eight protected categories and a complete comparison. For this narrow
   PE-5 publication, require exactly PE5_OUTPUT_DIRECTORY, PE5_CURRENT_JSON and
   PE5_CURRENT_DURABILITY_JSON, all in producer_state, present before and after.
   No fourth object, unrelated directory, code/configuration/security/lock/scheduler
   change or unexpected control change can use this disposition. Nothing grants a
   general producer_state exemption. Other mutation patterns remain unresolved.
4. Recompute each difference hash from the exact original base record using the
   executing helper's published algorithm: ASCII canonical JSON with sorted keys,
   compact separators, ensure_ascii=True, allow_nan=False, containing before_capture,
   after_capture and difference. Exclude only difference_sha256 and fields added
   after hashing (adjudication, adjudication_basis, review_references). Preserve all
   other original fields, values, list orders, nulls and decimal strings. Compare
   to both receipt and independently supplied expected hashes. Mismatched capture,
   difference or receipt bindings block acceptance; never replace them with expected
   values. This proves internal numerical binding, not production authenticity or
   an independently recalculated full-capture digest.
5. Review the complete original field differences. The directory must retain its
   identity and all fields except mtime/ctime; both regular files may undergo only
   the documented atomic inode replacement, bounded size and timestamp changes.
   Reject security/type/device/ownership/link-count changes, deletion/appearance,
   unsupported content/control changes or contradictory identities. Complete field
   differences establish equality of omitted unchanged fields, NOT their numeric
   values or safety. Do not invent those values. Establish file and directory safety
   from separately supplied checks bound to the same after-state. Equality plus
   valid bound after-state checks may establish unchanged safety without fabricating
   a prior tuple. A later unbound permission check proves neither endpoint's safety.
   The directory must have private 0700 ownership; files must be regular, nonlink,
   single-link, owner UID/GID1000/1000 and 0600, with accepted size bounds. Directory
   size/link-count equality is evidenced by complete differences; absent exact
   values stay unknown and are not claimed to satisfy the helper's tuple replay.
6. Examine separately supplied read-only PE-5 native validation under
   configured_association_store.Store.read_domain(OUTPUT) and descriptor() semantics:
   closed schema, canonical bytes, correct output domain, CONFIRMED, candidate null,
   exact confirmed descriptor/current digest and revision agreement, valid transaction
   identifier, and stable exact primary/sidecar identities before AND after validation.
   Bind both output hashes and file identities to the original receipt's after-state;
   record output evaluation time and transaction ID. Require validation's timing and
   identities to support this specific window, not a later replacement. CONFIRMED
   alone or a cron launch does not prove successful completion. No recovery, resync,
   producer run or lock-creating read_handoff() is part of evidence review.
7. Independently review writer authority and attribution. Cite the accepted PE-5.7
   activation and applicable PE-5 output/atomic/durability contract. Establish the
   observed scheduler's continued exact authorized scope, the relevant launch, the
   contract-valid completed transaction, after-state identity matches and all three
   effects as one coherent publication. Explain why the evidence supports the actual
   authorized PE5_COMPOSER operation, considering contradictory/alternative-writer
   evidence rather than inferring it from mutability or timestamps. Repository code
   establishes allowed operations, not which process acted in production. A valid
   transaction demonstrates output validity, not by itself actor identity. If actual
   writer authorization/attribution remains material and unresolved, decide
   INSUFFICIENT_EVIDENCE; do not replace this step with a mocked approval or boolean.
8. Record a NEW independent judgment with the fields below. No self-approval by the
   instrument, permission generated from the receipt, fabricated external reference,
   or automatic conversion to PASS is allowed. The reviewer must be independently
   authorized and identify its reasoning/evidence. Evidence identity references are
   documentary bindings, not authenticated signatures. No authentication service
   is implied. If the approval's provenance is not established, stop.

## Separate independent judgment format

This is a record template, not an issued permission or a new runtime schema.

- REVIEW_KIND=INDEPENDENT_REPOSITORY_EVIDENCE_JUDGMENT
- REVIEWER_AND_AUTHORITY: independently established identity and applicable authority
- ORIGINAL_RECEIPT_SHA256 and byte/canonical digest distinction
- ORIGINAL_EXECUTION_RESULT=INSUFFICIENT_EVIDENCE (for the historical second run)
- EXECUTING_HELPER_SHA256; INSTRUMENT_RELEASE_AND_SOURCE_AUTHORITY
- BEFORE_CAPTURE_SHA256; AFTER_CAPTURE_SHA256; all three original difference hashes
- EXTERNAL_EVIDENCE_REFERENCES_AND_CLASSES, including exact native validation,
  safety checks, current scheduler/launch, accepted activation and transaction bindings
- FUNCTIONAL_AND_PROTECTED_CHECKS: explicit findings, counts, scope and limitations
- WRITER_AUTHORIZATION_AND_ATTRIBUTION: independent reasoning, not an instrument claim
- PERMITTED_SCOPE: only the three identified objects, exact original differences,
  capture/receipt bindings and the validated publication transaction
- INDEPENDENT_DECISION=ACCEPT / REJECT / INSUFFICIENT_EVIDENCE, with reasons
- HELPER_REPLAY_PERFORMED=FALSE; ORIGINAL_RECEIPT_CHANGED=FALSE
- REMAINING_UNKNOWNS_AND_EVIDENCE_LIMITATIONS; separately authorized next gate

ACCEPT requires every material gate above to pass; no functional/protected failure,
missing authority or contradictory evidence may be waived. A separately supported
ACCEPT is a review decision about this bounded execution, not a claim that its
historical instrument printed PASS. Any later lifecycle documentation closure and
publication remain separate authorized work. No decision is issued by this candidate.

## Historical second-acceptance applicability

The original sanitized receipt supplies complete differences and capture bindings.
All three numerical difference hashes were independently reproduced with the old
and corrected published algorithms. It does NOT supply original full captures.
Recreating them or their complete digest preimages is neither possible from that
receipt nor required for the separate evidence judgment described here.

Separate OPERATOR_SUPPLIED observations include scheduler configuration/launch,
exact stable file after-identities, security checks and native validated completion
of dur_583e7b7692c94cb4a3f4e371569c4dcb, evaluated at
2026-10-20T03:32:02.396618Z. Those observations remain OPERATOR_SUPPLIED; they are
not authenticated permission or Codex production observations. Their adequacy,
exact bindings and writer attribution require the independent review above. This
preparation does not issue that review, rewrite the historical receipt, require
another classification execution, or close PE-6.4. Previously absent historical
source/content hashes remain NOT_CAPTURED, not backfilled with later observations.

The earlier suggestion to retain private captures for another classification run
was necessary only for helper replay, not a requirement established by PE-6.4 for
independent repository acceptance. This workflow does not authorize another run.
If external evidence cannot establish a material historical fact, retain the
original verdict and identify that precise gap; do not automatically rerun anything.

## Validation, privacy and maintenance

Use the established Windows stdin harness, shell-free PATH, HIOC_TEST_SHELL cleared,
sys.path[:0]=['tests','pi4/lib'], and no bytecode writes. Focused existing helper tests
exercise exact publication grants, absent/invalid authority, wrong writers/bindings,
missing/contradictory transaction evidence, fourth objects, unrelated paths, security
changes, replay mismatch, incomplete/truncated observations, failures and privacy.
Receipt-only review checks must consume actual build_report() output and the supplied
historical receipt after private captures are discarded. They must not mock an
approval into PASS or claim to authenticate an operator. Test-only native schema and
descriptor validation is not producer execution or production observation.

Test no-positive-evidence and independent failure gates without executing a classifier
in this checkpoint. Test attempted self-authorization as insufficient external authority,
not a new authentication protocol. Negative cases must remain blocked even if hashes
are recomputed for a contradictory fixture. Test success means reproducible evidence
checks and preservation of the external decision boundary, not issuance of approval.

No product, helper, instrument, import mechanism, dependency identity, inventory
exception, secure Reader, TTL, eight-category comparison, failure precedence, source
selection, producer, scheduler, lock, network or persistence behavior changes. There
is no new security subsystem, capture archive, daemon, interactive timeout or retry.
Review artifacts contain fixed identifiers, hashes, bounded metadata and sanitized
reasons only; private host/device data and full observations are not published.
Future checkpoints must apply their own governing contracts and exact scope; this
PE-5-specific review is not a generic permission for future producers or mutations.

## Source references

- HIOC_MASTER_PLAN.md:3-12,5905-5928,6198-6218: evidence classes, source/runtime
  separation and durable acceptance reporting. Master Plan is not changed here.
- PE6_CLASSIFICATION_CONTRACT_DESIGN.md:1056-1068: receipt followed by independent
  acceptance; missing authority and protected mismatches stop.
- PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md:374-395: accepted activation,
  historical scheduler identity and natural-cycle evidence limitations.
- PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md:835-867: exact outputs, security,
  scheduled command, confirmation, barriers, recovery and privacy boundaries.
- ../pi4/lib/hioc/configured_association_store.py:289-320,336-446: native descriptor,
  schema/canonical checks, confirmation and atomic publication implementation.
- ../tools/pe6_protected_state_evidence.py:3-8,63-81,130-132,257-265,300-318,
  323-345,388-424: private captures, external review boundary, runtime tuple checks,
  difference identity and independent outcomes. The existing API is not weakened.
- ../tools/pe6_hostname_acceptance.py:3-8,279-285,305-355: verified helper,
  independently supplied permissions, one evaluation, protected inspection and
  final receipt. No production procedure is executed or replaced here.

## Local preparation validation evidence

Windows repository validation at baseline
4911896bf34e56c64a174c8551e348c066d8f95b:

- 51 existing test_pe6_protected_state_evidence tests passed.
- 19 additional stdin unittest cases passed: original receipt numerical binding;
  actual generated report reviewed after capture disposal; missing authority;
  attempted self-permission; wrong capture/difference hashes; missing/fourth object;
  unrelated directory and security mutation despite recomputed hashes;
  incomplete/truncated/contradictory observations; functional failure; no positive
  classification; invocation/origin gates; privacy/no side effects; native valid
  schema/canonical/domain/descriptor/revision validation; malformed transaction;
  pending/candidate; wrong domain/digest/revision; noncanonical bytes; receipt
  preservation. Existing helper cases separately cover invalid writers and replay.
- Total 70 run, 70 passed, 0 failures, 0 errors, 0 skipped; class-level skips 0.
- The additional checklist evaluator was test-only stdin code, not a new production
  adjudicator. Its positive outcome was REQUIRES_INDEPENDENT_AUTHORIZATION_SAFETY_AND_TRANSACTION_REVIEW,
  never ACCEPT. No approval callback was mocked to return success.
- Native Store.read_domain()/descriptor() code ran against memory-backed fixture
  reads. Schema and descriptor checks were real; Windows fixture reads do not prove
  POSIX production permissions, successful physical durability or actual writer.
- No classifier or PE-5 composer execution, production access, private capture
  archive, code change, Master Plan change, commit, staging or push occurred.
- Original supplied JSON bytes, excluding the Markdown wrapper, SHA-256:
  923bfd707d278e5c0aa7099ee54fa2541c1633cda5a2f37220c0199b25cc27e4.
  The parsed receipt remains unchanged INSUFFICIENT_EVIDENCE. This digest is a
  repository calculation over OPERATOR_SUPPLIED evidence, not production attestation.

This preparation still requires independent review of the workflow and a separate
explicit historical evidence judgment before any acceptance claim. It creates no
new production authorization and no requirement to repeat classification.
