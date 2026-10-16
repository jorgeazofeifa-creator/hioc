"""T1 read-only project recovery; current observations are never cached."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from functools import lru_cache
import types
import unittest
from unittest.mock import patch

BASE = "94f014cea1d5216a1deeef9fd1d0a025f1c7083e"
ROOT = Path(__file__).resolve().parents[1]
CONTEXT = "docs/HIOC_PROJECT_CONTEXT.md"
RECORD = "governance/continuity/project-handoff.json"
SCHEMA = "governance/continuity/project-handoff.schema.json"
SCOPE = sorted(["README.md", "docs/HIOC_MASTER_PLAN.md", CONTEXT, RECORD, SCHEMA,
    "governance/continuity/t1-authorization.md",
    "governance/continuity/engineering-transition-issue-6.md",
    "tools/hioc_project_continuity.py", "tools/hioc-project-context.py",
    "tests/test_project_continuity.py", "tests/test_pe6_classification_implementation.py",
    "tests/test_pe5_service_association_caller.py"])
OWNERS = {
    "product_plan": "docs/HIOC_MASTER_PLAN.md", "overview": "docs/PROJECT.md",
    "runtime": "docs/OPERATIONS.md", "deployment": "docs/DEPLOYMENT.md",
    "architecture": "docs/ARCHITECTURE.md", "system": "docs/SYSTEM_REFERENCE.md",
    "data": "docs/DATA_MODEL.md", "mqtt": "docs/MQTT.md",
    "home_assistant": "docs/HOME_ASSISTANT.md",
    "pe6_design": "docs/PE6_CLASSIFICATION_CONTRACT_DESIGN.md",
    "pe6_implementation": "docs/PE6_CLASSIFICATION_IMPLEMENTATION.md"}
PRODUCT = dict(phase="Phase 7A ACTIVE", accepted_checkpoint="PE-6.1 COMPLETE/PASS",
    accepted_commit=BASE, next_checkpoint="PE-6.2 - PI3 Release-Source Synchronization",
    next_authorized=False, pe6_production_deployed_at_closure=False)
BOUNDARY = dict(codex="WINDOWS_REPOSITORY_ONLY", pi3_execution="OPERATOR_ONLY_SEPARATE_AUTHORIZATION",
    pi3_access=False, pi5_access=False, production_access=False, production_mutation=False,
    production_current_state="UNKNOWN", ha_access=False, mqtt_access=False, credential_access=False)
TRANSITION = dict(stage="T1", implementation="COMPLETE_REPOSITORY_IMPLEMENTATION",
    publication="VERIFY_FROM_GIT_NOT_THIS_RECORD", next_stage="T2", next_stage_authorized=False,
    sequence=["T1 continuity", "T2 binding audit", "T3 deterministic CI/test environments",
              "T4 bounded capability pilot", "T5 evidence-based consolidation"],
    immediate_after_acceptance="STOP; T2 requires separate authorization")
RECOVERY = dict(candidate_state="DERIVE_FROM_FRESH_GIT", accepted_unpublished_candidate=False,
    dirty_candidate="PRESERVE_AND_COMPARE; NEVER_RESET_OR_OVERWRITE",
    unavailable_repository="UNKNOWN_STOP; REQUEST_FILES_OR_VERIFIED_EXPORT",
    freshness="VERIFY_ALL_CURRENT_BYTES_AND_INDEX_EVERY_CALL; HISTORICAL_MODE_IS_SNAPSHOT_ONLY")


def require(ok, code):
    if not ok:
        raise ValueError(code)


def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def canonical(value): return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()


def git(*args):
    return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=ROOT,
                                   stderr=subprocess.PIPE)


def raw(path):
    return (ROOT / path).read_bytes().replace(b"\r\n", b"\n")


def _schema_helpers():
    # Reuse the established exact, typed, closed checkpoint-schema convention.
    sys.path.insert(0, str(ROOT / "tests")) if str(ROOT / "tests") not in sys.path else None
    from test_pe4_documentation_consistency_correction import closed_schema, validate
    return closed_schema, validate


def schema_for(record):
    closed, unused = _schema_helpers()
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "HIOC T1 derived continuity snapshot", **closed(record)}


def check_record(record, schema):
    require(schema == schema_for(record), "SCHEMA_MISMATCH")
    _schema_helpers()[1](record, schema)
    require(set(record) == {"schema_version", "project", "repository", "authorities", "product",
        "transition", "boundary", "recovery", "last_verified", "blockers", "unknowns",
        "pending_work", "authorized_paths", "artifacts"}, "RECORD_FIELDS")
    require(record["schema_version"] == "1.0", "SCHEMA_VERSION")
    require(record["project"] == "HIOC" and record["repository"] == "https://github.com/jorgeazofeifa-creator/hioc", "REPOSITORY_IDENTITY")
    require(canonical(record["authorities"]) == canonical(OWNERS), "DOCUMENT_OWNERSHIP")
    require(canonical(record["product"]) == canonical(PRODUCT), "PRODUCT_AUTHORITY")
    require(canonical(record["boundary"]) == canonical(BOUNDARY), "PRODUCTION_ASSUMPTION")
    require(canonical(record["transition"]) == canonical(TRANSITION), "TRANSITION_AUTHORIZATION")
    require(canonical(record["recovery"]) == canonical(RECOVERY), "CANDIDATE_TRANSITION")
    require(canonical(record["last_verified"]) == canonical(dict(evidence_class="DIRECT_OBSERVATION", scope="WINDOWS_REPOSITORY_AT_T1_START",
        commit=BASE, branch="main", head_equals_origin_main=True, clean=True,
        limitation="HISTORICAL_OBSERVATION; REVERIFY_LIVE_STATE")), "OBSERVATION_PROVENANCE")
    require(record["blockers"] == [] and record["unknowns"] == ["Current production state", "Future checkpoint authorization"], "UNKNOWN_PROVENANCE")
    require(record["pending_work"] == ["T2 through T5: separate authorization", "PE-6.2: separate authorization", "Phase 7B Active Discovery postponed"], "PENDING_AUTHORITY")
    require(record["authorized_paths"] == SCOPE, "SCOPE")
    require([x["path"] for x in record["artifacts"]] == [p for p in SCOPE if p not in (RECORD, SCHEMA)], "ARTIFACT_SCOPE")
    for item in record["artifacts"]:
        require(set(item) == {"path", "sha256", "git_blob", "mode"} and
                re.fullmatch("[0-9a-f]{64}", item["sha256"]) and re.fullmatch("[0-9a-f]{40}", item["git_blob"]) and item["mode"] == "100644", "ARTIFACT_IDENTITY")
    return record


def privacy(data):
    text = data.decode("utf8")
    require(not re.search(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----|(?:password|access_token|api_key)\s*[:=]\s*[^\s;]+|(?:mqtt|https?)://[^/\s]+:[^/\s]+@", text, re.I), "SENSITIVE_INFORMATION")


def tree(commit, run=git):
    require(re.fullmatch("[0-9a-f]{40}", commit) is not None, "COMMIT_IDENTITY")
    rows = {}
    for row in run("ls-tree", "-r", "-z", commit).split(b"\0"):
        if row:
            info, path = row.split(b"\t", 1)
            mode, kind, oid = info.decode().split()
            require(kind == "blob", "UNSUPPORTED_TREE_ENTRY")
            rows[path.decode()] = (mode, oid)
    require(rows, "MISSING_COMMIT")
    return rows


def inspect(record, schema, read, entries, run=git):
    check_record(record, schema)
    baseline = tree(BASE, run)
    require(set(entries) == set(baseline) | set(SCOPE), "UNEXPECTED_PATH")
    for path, identity in baseline.items():
        if path not in SCOPE:
            require(entries.get(path) == identity and blob(read(path)) == identity[1], "PROTECTED_BASELINE_ARTIFACT")
    for item in record["artifacts"]:
        data = read(item["path"])
        require((sha(data), blob(data)) == (item["sha256"], item["git_blob"]), "CURRENT_ARTIFACT_IDENTITY")
        require(entries.get(item["path"]) == (item["mode"], item["git_blob"]), "STAGED_ARTIFACT_IDENTITY")
        privacy(data)
    for path in [RECORD, SCHEMA]:
        require(entries.get(path) == ("100644", blob(read(path))), "STAGED_GOVERNANCE_IDENTITY")
    for path in OWNERS.values():
        require(path in entries and read(path), "MISSING_AUTHORITY")
    master = read(OWNERS["product_plan"]).decode()
    section = master.split("## Next Planned Task\n", 1)[1].split("### Historical", 1)[0]
    require(section.lstrip().startswith("### PE-6.2 - PI3 Release-Source Synchronization") and
        all(value in section for value in ["Phase 7A ACTIVE", "PE6_1_STATUS=COMPLETE/PASS", "PE6_2_STARTED=FALSE", "PE6_PRODUCTION_DEPLOYED=FALSE", "Separate authorization is required for PE-6.2"]), "MASTER_PLAN_CONTRADICTION")
    require("## Engineering Transition T1 - Durable Project Continuity" in master, "STALE_MASTER_PLAN")
    context = read(CONTEXT).decode()
    require(all(value in context for value in [BASE, "UNKNOWN -> VERIFY -> ESTABLISH EVIDENCE -> DECIDE -> ACT", "OPERATOR_SUPPLIED", "T2", RECORD, "Continue HIOC.", "docs/PROJECT.md"]), "STALE_CONTEXT")
    # The existing product plan is retained byte-for-byte; only the T1 notice is appended.
    require(read(OWNERS["product_plan"]).startswith(run("show", BASE + ":" + OWNERS["product_plan"])), "HISTORICAL_MASTER_PLAN_CHANGED")
    return record


def validate_current(read=None, run=None):
    read = raw if read is None else read
    run = git if run is None else run
    # No persistent current-state cache. All bytes, Git scope and index are read afresh.
    require(os.name == "nt", "WINDOWS_REPOSITORY_ONLY")
    require(run("rev-parse", "--show-toplevel").decode().strip().replace("\\", "/").lower() == str(ROOT).replace("\\", "/").lower(), "REPOSITORY_ROOT")
    remote = run("remote", "get-url", "origin").decode().strip()
    require(remote in ["https://github.com/jorgeazofeifa-creator/hioc.git", "git@github.com:jorgeazofeifa-creator/hioc.git"], "REPOSITORY_IDENTITY")
    require(run("branch", "--show-current").decode().strip() == "main", "BRANCH")
    head = run("rev-parse", "HEAD").decode().strip()
    require(run("merge-base", BASE, head).decode().strip() == BASE, "STALE_BASELINE")
    origin = run("rev-parse", "origin/main").decode().strip()
    require(origin in (BASE, head) and run("rev-list", "--left-right", "--count", "HEAD...origin/main").decode().split() in [["0", "0"], ["1", "0"]], "REMOTE_AUTHORITY_REQUIRES_VERIFICATION")
    changed = set(run("diff", "--name-only", BASE).decode().splitlines())
    untracked = set(run("ls-files", "--others", "--exclude-standard").decode().splitlines())
    require(changed | untracked == set(SCOPE), "UNEXPECTED_PATH")
    index = {}
    for row in run("ls-files", "--stage").decode().splitlines():
        info, path = row.split("\t", 1); mode, oid, stage = info.split()
        require(stage == "0", "UNMERGED_INDEX")
        index[path] = (mode, oid)
    require(not untracked, "UNSTAGED_CANDIDATE; PRESERVE_AND_STAGE_ONLY_AUTHORIZED_PATHS")
    r, s = json.loads(read(RECORD)), json.loads(read(SCHEMA))
    require(read(RECORD) == canonical(r) and read(SCHEMA) == canonical(s), "CANONICAL_HANDOFF")
    inspect(r, s, read, index, run)
    clean = not run("status", "--porcelain").strip()
    require((head == BASE and not clean) or (head != BASE and clean), "CANDIDATE_TRANSITION")
    return r


def validate_snapshot(commit, run=None):
    require(type(commit) is str and re.fullmatch("[0-9a-f]{40}", commit) is not None, "COMMIT_IDENTITY")
    run = git if run is None else run
    require(run("merge-base", BASE, commit).decode().strip() == BASE, "STALE_BASELINE")
    entries = tree(commit, run)
    read = lambda path: run("show", commit + ":" + path)
    r, s = json.loads(read(RECORD)), json.loads(read(SCHEMA))
    require(read(RECORD) == canonical(r) and read(SCHEMA) == canonical(s), "CANONICAL_HANDOFF")
    inspect(r, s, read, entries, run)
    return r


def recover(commit=None):
    r = validate_snapshot(commit) if commit else validate_current()
    observed = None
    action = "STOP; separate authorization required for T2 or PE-6.2"
    if not commit:
        head = git("rev-parse", "HEAD").decode().strip()
        origin = git("rev-parse", "origin/main").decode().strip()
        counts = git("rev-list", "--left-right", "--count", "HEAD...origin/main").decode().split()
        state = "STAGED_UNPUBLISHED_T1" if head == BASE else "COMMITTED_SYNCHRONIZED" if head == origin else "COMMITTED_UNPUBLISHED_T1"
        observed = dict(evidence_class="DIRECT_OBSERVATION", scope="WINDOWS_REPOSITORY", head=head,
            origin_main=origin, branch=git("branch", "--show-current").decode().strip(),
            ahead=int(counts[0]), behind=int(counts[1]),
            working_tree_clean=not git("status", "--porcelain").strip(),
            staging_empty=not git("diff", "--cached", "--name-only").strip(),
            untracked_path_count=len(git("ls-files", "--others", "--exclude-standard").decode().splitlines()),
            candidate_state=state, independent_github_verification="NOT_ESTABLISHED_BY_LOCAL_TOOL")
        if state == "STAGED_UNPUBLISHED_T1": action = "FINISH_AUTHORIZED_T1_VALIDATION_AND_PUBLICATION; NO_NEXT_STAGE"
        elif state == "COMMITTED_UNPUBLISHED_T1": action = "VERIFY_T1_ACCEPTANCE_EVIDENCE_AND_COMMIT_BEFORE_AUTHORIZED_PUBLICATION; NO_NEXT_STAGE"
        else: action = "VERIFY_GITHUB_COMMIT_AND_ARTIFACTS_IF_NOT_ALREADY_ESTABLISHED; STOP_BEFORE_T2_OR_PE62"
    return dict(result="PASS_HISTORICAL_SNAPSHOT" if commit else "PASS_CURRENT_CONTINUITY",
        mission="Help the operator understand what is happening, why, impact and next action",
        product=r["product"], transition=r["transition"], boundary=r["boundary"],
        owners=r["authorities"], candidate_recovery=r["recovery"],
        live_state="NOT_OBSERVED" if commit else "FRESHLY_VERIFIED_WINDOWS_REPOSITORY",
        production_state="UNKNOWN", observed_repository=observed, next_action=action)


@lru_cache(maxsize=1)
def historical_implementation_module():
    """Only immutable PE-6.1 code/objects are cached; no current-state acceptance."""
    path = "tests/test_pe6_classification_implementation.py"
    module = types.ModuleType("test_pe6_classification_implementation")
    module.__file__ = str(ROOT / path)
    exec(compile(git("show", BASE + ":" + path), module.__file__, "exec"), module.__dict__)
    original = module.git
    entries = tree(BASE)
    stage = "".join(mode + " " + oid + " 0\t" + p + "\n" for p, (mode, oid) in sorted(entries.items())).encode()
    def snapshot_git(*args):
        if args in [("diff", "--name-only", module.BASE), ("diff", "--cached", "--name-only", module.BASE)]:
            return original("diff", "--name-only", module.BASE, BASE)
        if args == ("ls-files", "--others", "--exclude-standard"): return b""
        if args == ("ls-files", "--stage"): return stage
        return original(*args)
    module.git = snapshot_git
    @lru_cache(maxsize=None)
    def accepted_raw(p): return original("show", BASE + ":" + p)
    module.raw = accepted_raw
    return module


@lru_cache(maxsize=1)
def accepted_implementation():
    return canonical(historical_implementation_module().implementation_successor())


def current_implementation():
    r = validate_current()
    historical = json.loads(accepted_implementation())
    mapping = {x["path"]: x for x in historical["artifacts"]}
    mapping.update({x["path"]: x for x in r["artifacts"]})
    # Derived current artifact view; the historical JSON/schema are never rewritten.
    historical["artifacts"] = list(mapping.values())
    return historical


class HistoricalImplementationSuite(unittest.TestSuite):
    def run(self, result, debug=False):
        module = historical_implementation_module()
        with patch.dict(sys.modules, test_pe6_classification_implementation=module):
            return super().run(result, debug)


def historical_implementation_tests(loader):
    module = historical_implementation_module()
    return HistoricalImplementationSuite(loader.loadTestsFromTestCase(module.ImplementationGovernanceTests))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", help="explicit immutable snapshot only; no live-state claim")
    args = parser.parse_args()
    try:
        print(json.dumps(recover(args.commit), sort_keys=True))
    except (ValueError, TypeError, OSError, KeyError, IndexError, subprocess.CalledProcessError, json.JSONDecodeError):
        print(json.dumps(dict(result="UNKNOWN_STOP", action="PRESERVE; VERIFY_AUTHORITY_AND_ARTIFACTS", production_state="UNKNOWN")))
        return 1
    return 0
