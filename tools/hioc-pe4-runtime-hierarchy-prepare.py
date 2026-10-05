#!/usr/bin/env python3
"""PE-4.0B.2a-D-PREP: establish only the trusted Action D hierarchy."""

import argparse
import json
import os

from hioc_pe4_runtime_common import *


ACTION = "PE-4.0B.2a-D-PREP"
EVIDENCE_MAX_BYTES = 4096
EVIDENCE_PREFIX = "hioc-pe4-runtime-hierarchy-prepare-"
EVIDENCE_RE = re.compile(r"^/tmp/hioc-pe4-runtime-hierarchy-prepare-[A-Za-z0-9]{8}$")
DIAGNOSTIC_STAGES = frozenset(("TARGET_IDENTITY", "SOURCE_IDENTITY", "RUNTIME_ANCHOR",
    "RUNTIME_PARENT", "RUNTIME_ROOT", "ENVIRONMENTS", "FINAL_VALIDATION",
    "EVIDENCE_PUBLICATION", "INTERNAL"))
DIAGNOSTIC_OPERATIONS = frozenset(("TARGET", "REPOSITORY", "OPEN_ANCHOR",
    "ENSURE_RUNTIME", "ENSURE_PE4", "ENSURE_ENVIRONMENTS", "REVALIDATE",
    "PUBLISH_EVIDENCE", "INTERNAL"))


def diagnostic_exception(exc: BaseException) -> tuple[str, str]:
    if isinstance(exc, Failure): return "GOVERNED_FAILURE", "NONE"
    if isinstance(exc, PermissionError): name = "PERMISSION_ERROR"
    elif isinstance(exc, FileNotFoundError): name = "FILE_NOT_FOUND"
    elif isinstance(exc, FileExistsError): name = "FILE_EXISTS"
    elif isinstance(exc, NotADirectoryError): name = "NOT_A_DIRECTORY"
    elif isinstance(exc, IsADirectoryError): name = "IS_A_DIRECTORY"
    elif isinstance(exc, OSError): name = "OS_ERROR"
    elif isinstance(exc, ValueError): name = "VALUE_ERROR"
    else: name = "OTHER"
    value = getattr(exc, "errno", None)
    return name, str(value) if isinstance(value, int) and value >= 0 else "NONE"


def emit_state(state: dict[str, str]) -> None:
    for key in ("RUNTIME_PARENT_STATE", "RUNTIME_ROOT_STATE", "ENVIRONMENTS_STATE",
                "CREATED_RUNTIME_PARENT", "CREATED_RUNTIME_ROOT", "CREATED_ENVIRONMENTS",
                "CLEANUP_STATE", "EVIDENCE_STATE"):
        print(f"{key}={state[key]}")


def document(commit: str, state: dict[str, str], runtime: OwnedDirectory,
             root: OwnedDirectory, environments: OwnedDirectory) -> dict[str, object]:
    value = {"schema_version": "1.0", "action": ACTION, "governance_commit": commit,
        "result": "PASS", "error_code": "NONE", "failure_stage": "COMPLETE",
        "rollback_recommended": False, "runtime_parent_state": state["RUNTIME_PARENT_STATE"],
        "runtime_root_state": state["RUNTIME_ROOT_STATE"],
        "environments_state": state["ENVIRONMENTS_STATE"],
        "created_runtime_parent": state["CREATED_RUNTIME_PARENT"] == "TRUE",
        "created_runtime_root": state["CREATED_RUNTIME_ROOT"] == "TRUE",
        "created_environments": state["CREATED_ENVIRONMENTS"] == "TRUE",
        "runtime_parent_mode": format(runtime.mode, "04o"), "runtime_root_mode": format(root.mode, "04o"),
        "environments_mode": format(environments.mode, "04o"),
        "device_relationship": "RUNTIME_TO_PE4_SAME_DEVICE;PE4_TO_ENVIRONMENTS_SAME_DEVICE",
        "cleanup_state": state["CLEANUP_STATE"]}
    if len(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()) + 1 > EVIDENCE_MAX_BYTES:
        raise Failure("EVIDENCE_DOCUMENT_TOO_LARGE", "EVIDENCE_PUBLICATION")
    return value


def main() -> int:
    state = {"RUNTIME_PARENT_STATE": "NOT_REACHED", "RUNTIME_ROOT_STATE": "NOT_REACHED",
        "ENVIRONMENTS_STATE": "NOT_REACHED", "CREATED_RUNTIME_PARENT": "FALSE",
        "CREATED_RUNTIME_ROOT": "FALSE", "CREATED_ENVIRONMENTS": "FALSE",
        "CLEANUP_STATE": "NOT_APPLICABLE", "EVIDENCE_STATE": "NOT_CREATED"}
    anchor = runtime = root = environments = evidence_root = evidence = None
    stage, operation, commit = "INTERNAL", "INTERNAL", None
    old_umask = os.umask(0o027)
    try:
        stage, operation = "TARGET_IDENTITY", "TARGET"; verify_pi3()
        parser = argparse.ArgumentParser()
        parser.add_argument("--governance-commit", required=True)
        args = parser.parse_args(); commit = args.governance_commit
        stage, operation = "SOURCE_IDENTITY", "REPOSITORY"
        verify_repository(SOURCE, commit, ("tools/hioc-pe4-runtime-hierarchy-prepare.py",
                                            "tools/hioc_pe4_runtime_common.py"))
        stage, operation = "RUNTIME_ANCHOR", "OPEN_ANCHOR"
        anchor = open_trusted_owned_path_bound(RUNTIME, "RUNTIME_ANCHOR")
        stage, operation = "RUNTIME_PARENT", "ENSURE_RUNTIME"
        revalidate_path_bound_directory(anchor, stage)
        runtime, created = ensure_owned_named_child(anchor, "runtime", 0o750, stage,
                                                     require_same_device=False)
        revalidate_path_bound_directory(anchor, stage)
        state["RUNTIME_PARENT_STATE"] = "CREATED_CONFIRMED" if created else "PREEXISTING_COMPLIANT"
        state["CREATED_RUNTIME_PARENT"] = "TRUE" if created else "FALSE"
        stage, operation = "RUNTIME_ROOT", "ENSURE_PE4"
        revalidate_path_bound_directory(runtime, stage)
        root, created = ensure_owned_named_child(runtime, "pe4", 0o750, stage)
        revalidate_path_bound_directory(runtime, stage)
        state["RUNTIME_ROOT_STATE"] = "CREATED_CONFIRMED" if created else "PREEXISTING_COMPLIANT"
        state["CREATED_RUNTIME_ROOT"] = "TRUE" if created else "FALSE"
        stage, operation = "ENVIRONMENTS", "ENSURE_ENVIRONMENTS"
        revalidate_path_bound_directory(root, stage)
        environments, created = ensure_owned_named_child(root, "environments", 0o750, stage)
        revalidate_path_bound_directory(root, stage)
        state["ENVIRONMENTS_STATE"] = "CREATED_CONFIRMED" if created else "PREEXISTING_COMPLIANT"
        state["CREATED_ENVIRONMENTS"] = "TRUE" if created else "FALSE"
        stage, operation = "FINAL_VALIDATION", "REVALIDATE"
        for directory in (anchor, runtime, root, environments): revalidate_path_bound_directory(directory, stage)
        stage, operation = "EVIDENCE_PUBLICATION", "PUBLISH_EVIDENCE"
        revalidate_path_bound_directory(environments, stage)
        evidence_root = open_tmp_root(stage)
        evidence = create_owned_child(evidence_root, EVIDENCE_PREFIX, 0o700, stage)
        state["EVIDENCE_STATE"] = "CREATED"
        publish_owned_json(evidence, "result.json", document(commit, state, runtime, root, environments), stage,
                           max_bytes=EVIDENCE_MAX_BYTES)
        state["EVIDENCE_STATE"] = "CONFIRMED"
        revalidate_path_bound_directory(environments, "FINAL_VALIDATION")
        emit_state(state); terminal("PASS", "NONE", "COMPLETE", False, evidence.path)
        print("STOP_REQUIRED=TRUE")
        return 0
    except NamedChildFailure as exc:
        if operation == "ENSURE_RUNTIME":
            state["RUNTIME_PARENT_STATE"] = "CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED"
        elif operation == "ENSURE_PE4":
            state["RUNTIME_ROOT_STATE"] = "CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED"
        elif operation == "ENSURE_ENVIRONMENTS":
            state["ENVIRONMENTS_STATE"] = "CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED"
        emit_state(state); terminal("FAIL", exc.code, exc.stage, False)
        klass, errno = diagnostic_exception(exc)
        print(f"DIAGNOSTIC_STAGE={stage}\nDIAGNOSTIC_OPERATION={operation}\nEXCEPTION_CLASS={klass}\nERRNO={errno}\nSTOP_REQUIRED=TRUE")
        return 1
    except Failure as exc:
        if stage == "EVIDENCE_PUBLICATION": state["EVIDENCE_STATE"] = "UNCONFIRMED"
        emit_state(state); terminal("FAIL", exc.code, exc.stage, exc.rollback,
                                    evidence.path if state["EVIDENCE_STATE"] == "CONFIRMED" else None)
        klass, errno = diagnostic_exception(exc)
        print(f"DIAGNOSTIC_STAGE={stage}\nDIAGNOSTIC_OPERATION={operation}\nEXCEPTION_CLASS={klass}\nERRNO={errno}\nSTOP_REQUIRED=TRUE")
        return 1
    except Exception as exc:
        if stage == "EVIDENCE_PUBLICATION": state["EVIDENCE_STATE"] = "UNCONFIRMED"
        emit_state(state); terminal("FAIL", "UNEXPECTED_ERROR", "UNEXPECTED", False)
        klass, errno = diagnostic_exception(exc)
        print(f"DIAGNOSTIC_STAGE={stage}\nDIAGNOSTIC_OPERATION={operation}\nEXCEPTION_CLASS={klass}\nERRNO={errno}\nSTOP_REQUIRED=TRUE")
        return 1
    finally:
        os.umask(old_umask)
        for directory in (evidence, evidence_root, environments, root, runtime, anchor):
            if directory is not None:
                try: directory.close()
                except OSError: pass


if __name__ == "__main__":
    raise SystemExit(main())
