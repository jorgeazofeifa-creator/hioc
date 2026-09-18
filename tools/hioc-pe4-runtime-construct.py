#!/usr/bin/env python3
"""PE-4.0B.2a-D: descriptor-bound private venv construction and offline install."""

import argparse
import json
import os
import pathlib
import re

from hioc_pe4_runtime_common import *


DIAGNOSTIC_STAGES = frozenset(("INPUT_VALIDATION", "INPUT_SNAPSHOT", "SEALED_LOCK",
    "RUNTIME_PARENT_VALIDATION", "RUNTIME_ROOT_VALIDATION", "ENVIRONMENTS_ROOT_VALIDATION",
    "CONSTRUCTION_ALLOCATION", "VENV_CREATION", "VENV_FILESYSTEM", "RUNTIME_IDENTITY",
    "PIP_CAPABILITY", "OFFLINE_INSTALL", "DISTRIBUTION_VALIDATION",
    "CONSTRUCTION_CONFIRMATION", "INPUT_SNAPSHOT_CLEANUP", "EVIDENCE_PUBLICATION",
    "ELIGIBILITY_PUBLICATION", "CLEANUP", "INTERNAL"))
DIAGNOSTIC_OPERATIONS = frozenset(("ARGUMENTS", "REPOSITORY", "TRANSFER_SNAPSHOT",
    "LOCK_STAT", "SEALED_LOCK", "OPEN_RUNTIME_PARENT", "OPEN_RUNTIME_ROOT",
    "OPEN_ENVIRONMENTS_ROOT", "CREATE_CONSTRUCTION", "CREATE_VENV", "VALIDATE_VENV",
    "PROBE_RUNTIME", "CHECK_PIP", "INSTALL_OFFLINE", "VALIDATE_DISTRIBUTIONS",
    "CONFIRM_CONSTRUCTION", "CLEAN_SNAPSHOT", "PUBLISH_SUCCESS_EVIDENCE",
    "PUBLISH_ELIGIBILITY", "FAILURE_EVIDENCE", "INTERNAL"))
FAILURE_EVIDENCE_RE = re.compile(r"^/tmp/hioc-pe4-runtime-construct-failure-[A-Za-z0-9]{8}$")


def _diagnostic_exception(exc: BaseException) -> tuple[str, str]:
    if isinstance(exc, Failure): return "GOVERNED_FAILURE", "NONE"
    if isinstance(exc, PermissionError): name = "PERMISSION_ERROR"
    elif isinstance(exc, FileNotFoundError): name = "FILE_NOT_FOUND"
    elif isinstance(exc, FileExistsError): name = "FILE_EXISTS"
    elif isinstance(exc, NotADirectoryError): name = "NOT_A_DIRECTORY"
    elif isinstance(exc, IsADirectoryError): name = "IS_A_DIRECTORY"
    elif isinstance(exc, TimeoutError): name = "TIMEOUT"
    elif isinstance(exc, OSError): name = "OS_ERROR"
    elif isinstance(exc, ValueError): name = "VALUE_ERROR"
    elif isinstance(exc, RuntimeError): name = "RUNTIME_ERROR"
    else: name = "OTHER"
    value = getattr(exc, "errno", None)
    return name, str(value) if isinstance(value, int) and value >= 0 else "NONE"


def _failure_document(commit: str, state: dict[str, str], stage: str, operation: str,
                      exc: BaseException, error_code: str, failure_stage: str) -> dict[str, object]:
    if stage not in DIAGNOSTIC_STAGES or operation not in DIAGNOSTIC_OPERATIONS:
        raise Failure("DIAGNOSTIC_CONTEXT_INVALID", "INTERNAL")
    exception_class, errno = _diagnostic_exception(exc)
    document = {"schema_version": "1.0", "action": "PE-4.0B.2a-D",
        "record_type": "SANITIZED_FAILURE", "governance_commit": commit,
        "result": "FAIL", "error_code": error_code, "failure_stage": failure_stage,
        "rollback_recommended": False,
        "construction_created": state["CONSTRUCTION_CREATED"] == "TRUE",
        "construction_confirmed": state["CONSTRUCTION_CONFIRMED"] == "TRUE",
        "construction_retained": state["CONSTRUCTION_RETAINED"] == "TRUE",
        "input_snapshot_created": state["INPUT_SNAPSHOT_CREATED"] == "TRUE",
        "input_snapshot_retained": state["INPUT_SNAPSHOT_RETAINED"] == "TRUE",
        "cleanup_state": state["CLEANUP_STATE"], "diagnostic_stage": stage,
        "diagnostic_operation": operation, "exception_class": exception_class, "errno": errno}
    if len(json.dumps(document, sort_keys=True, separators=(",", ":")).encode()) > 4096:
        raise Failure("FAILURE_EVIDENCE_TOO_LARGE", "FAILURE_EVIDENCE")
    return document


def _emit_diagnostics(stage: str, operation: str, exc: BaseException, state: dict[str, str]) -> None:
    exception_class, errno = _diagnostic_exception(exc)
    print(f"DIAGNOSTIC_STAGE={stage}"); print(f"DIAGNOSTIC_OPERATION={operation}")
    print(f"EXCEPTION_CLASS={exception_class}"); print(f"ERRNO={errno}")
    print(f"CLEANUP_EXCEPTION_CLASS={state['CLEANUP_EXCEPTION_CLASS']}")
    print(f"CLEANUP_ERRNO={state['CLEANUP_ERRNO']}")
    print(f"FAILURE_EVIDENCE_STATE={state['FAILURE_EVIDENCE_STATE']}")
    print(f"FAILURE_EVIDENCE_PUBLICATION={state['FAILURE_EVIDENCE_PUBLICATION']}")
    path = state.get("FAILURE_EVIDENCE_DIR")
    if path and FAILURE_EVIDENCE_RE.fullmatch(path): print(f"FAILURE_EVIDENCE_DIR={path}")


def _publish_failure_evidence(commit: str, state: dict[str, str], stage: str, operation: str,
                              exc: BaseException, error_code: str, failure_stage: str) -> None:
    root = evidence = None
    try:
        root = open_tmp_root("FAILURE_EVIDENCE_PUBLICATION")
        evidence = create_owned_child(root, "hioc-pe4-runtime-construct-failure-", 0o700,
                                      "FAILURE_EVIDENCE_PUBLICATION")
        state["FAILURE_EVIDENCE_DIR"] = str(evidence.path)
        document = _failure_document(commit, state, stage, operation, exc, error_code, failure_stage)
        publish_owned_json(evidence, "failure-result.json", document, "FAILURE_EVIDENCE_PUBLICATION")
        state["FAILURE_EVIDENCE_STATE"] = "CONFIRMED"
        state["FAILURE_EVIDENCE_PUBLICATION"] = "CONFIRMED"
    except Exception:
        state["FAILURE_EVIDENCE_STATE"] = "UNCONFIRMED"
        state["FAILURE_EVIDENCE_PUBLICATION"] = "FAILED"
    finally:
        if evidence is not None: evidence.close()
        if root is not None: root.close()


def _runtime_probe(construction: OwnedDirectory, environment: dict[str, str]) -> dict[str, object]:
    code = r'''import json,os,platform,sys,sysconfig
print(json.dumps({"implementation":platform.python_implementation(),"version":platform.python_version(),"soabi":sysconfig.get_config_var("SOABI"),"prefix":sys.prefix,"base_prefix":sys.base_prefix,"base_executable":os.path.realpath(sys._base_executable),"no_user_site":bool(sys.flags.no_user_site),"paths":sys.path,"real_paths":[os.path.realpath(p) for p in sys.path]},sort_keys=True))'''
    result = run(["./bin/python", "-I", "-c", code], "RUNTIME_IDENTITY",
                 cwd=f"/proc/self/fd/{construction.fd}", pass_fds=(construction.fd,),
                 env=environment)
    try:
        value = json.loads(result.stdout)
    except (ValueError, json.JSONDecodeError):
        raise Failure("RUNTIME_PROBE_INVALID", "RUNTIME_IDENTITY")
    if (value.get("implementation") != "CPython" or value.get("version") != "3.11.2"
            or value.get("soabi") != "cpython-311-aarch64-linux-gnu"
            or value.get("prefix") == value.get("base_prefix")
            or value.get("base_executable") != os.path.realpath("/usr/bin/python3")
            or value.get("no_user_site") is not True
            or any("site-packages" in item and not item.startswith(str(construction.path) + os.sep)
                   for item in value.get("real_paths", []))):
        raise Failure("RUNTIME_IDENTITY_MISMATCH", "RUNTIME_IDENTITY")
    return value


def _emit_state(state: dict[str, str]) -> None:
    for key in ("CONSTRUCTION_CREATED", "CONSTRUCTION_CONFIRMED", "CONSTRUCTION_RETAINED",
                "INPUT_SNAPSHOT_CREATED", "INPUT_SNAPSHOT_RETAINED", "EVIDENCE_STATE",
                "ACTION_D_ELIGIBILITY", "CLEANUP_STATE"):
        print(f"{key}={state[key]}")


def main() -> int:
    state = {"CONSTRUCTION_CREATED": "FALSE", "CONSTRUCTION_CONFIRMED": "FALSE",
             "CONSTRUCTION_RETAINED": "FALSE", "INPUT_SNAPSHOT_CREATED": "FALSE",
             "INPUT_SNAPSHOT_RETAINED": "FALSE", "EVIDENCE_STATE": "NOT_CREATED",
             "ACTION_D_ELIGIBILITY": "NOT_CONFIRMED", "CLEANUP_STATE": "NOT_REQUIRED",
             "CLEANUP_EXCEPTION_CLASS": "NONE", "CLEANUP_ERRNO": "NONE",
             "FAILURE_EVIDENCE_STATE": "NOT_CREATED",
             "FAILURE_EVIDENCE_PUBLICATION": "NOT_ATTEMPTED"}
    construction = snapshot = evidence = None
    lock_fd = -1
    runtime_parent = runtime_root = environment_root = evidence_root = None
    diagnostic_stage, diagnostic_operation = "INTERNAL", "INTERNAL"
    governance_commit = None
    old_umask = os.umask(0o027)
    try:
        verify_pi3()
        diagnostic_stage, diagnostic_operation = "INPUT_VALIDATION", "ARGUMENTS"
        parser = argparse.ArgumentParser()
        parser.add_argument("--governance-commit", required=True)
        parser.add_argument("--transfer-directory", required=True)
        args = parser.parse_args()
        governance_commit = args.governance_commit
        diagnostic_operation = "REPOSITORY"
        verify_repository(SOURCE, args.governance_commit, (
            "tools/hioc-pe4-runtime-construct.py", "tools/hioc_pe4_runtime_common.py",
            "requirements-pe4.lock"))
        diagnostic_stage, diagnostic_operation = "INPUT_SNAPSHOT", "TRANSFER_SNAPSHOT"
        snapshot = create_action_d_input_snapshot(args.transfer_directory)
        state["INPUT_SNAPSHOT_CREATED"] = "TRUE"
        diagnostic_operation = "LOCK_STAT"
        lock_size = os.stat("requirements-pe4.lock", dir_fd=snapshot.fd,
                            follow_symlinks=False).st_size
        diagnostic_stage, diagnostic_operation = "SEALED_LOCK", "SEALED_LOCK"
        lock_fd = sealed_snapshot_file(snapshot, "requirements-pe4.lock", lock_size, LOCK_SHA256)
        diagnostic_stage, diagnostic_operation = "RUNTIME_PARENT_VALIDATION", "OPEN_RUNTIME_PARENT"
        runtime_parent = open_trusted_owned_parent(RUNTIME_ROOT.parent, "ENVIRONMENT_ROOT")
        diagnostic_stage, diagnostic_operation = "RUNTIME_ROOT_VALIDATION", "OPEN_RUNTIME_ROOT"
        runtime_root = open_owned_directory(RUNTIME_ROOT, 0o750, "ENVIRONMENT_ROOT",
                                            parent=runtime_parent)
        diagnostic_stage, diagnostic_operation = "ENVIRONMENTS_ROOT_VALIDATION", "OPEN_ENVIRONMENTS_ROOT"
        environment_root = open_owned_directory(ENVIRONMENT_ROOT, 0o750,
                                                "ENVIRONMENT_ROOT", parent=runtime_root)
        diagnostic_stage, diagnostic_operation = "CONSTRUCTION_ALLOCATION", "CREATE_CONSTRUCTION"
        construction = create_owned_child(environment_root,
            f".construct-{VERSIONED_NAME}-", 0o750, "CONSTRUCTION_CREATION")
        state["CONSTRUCTION_CREATED"] = "TRUE"
        environment = action_d_subprocess_environment()
        work = f"/proc/self/fd/{construction.fd}"
        inputs = f"/proc/self/fd/{snapshot.fd}"
        diagnostic_stage, diagnostic_operation = "VENV_CREATION", "CREATE_VENV"
        run(["/usr/bin/python3", "-I", "-m", "venv", "--copies", "."],
            "VENV_CREATION", timeout=120, cwd=work, pass_fds=(construction.fd,), env=environment)
        os.fchmod(construction.fd, 0o750)
        diagnostic_stage, diagnostic_operation = "VENV_FILESYSTEM", "VALIDATE_VENV"
        revalidate_owned_directory(construction, "VENV_FILESYSTEM")
        validate_venv_symlinks(construction)
        diagnostic_stage, diagnostic_operation = "RUNTIME_IDENTITY", "PROBE_RUNTIME"
        _runtime_probe(construction, environment)
        diagnostic_stage, diagnostic_operation = "PIP_CAPABILITY", "CHECK_PIP"
        help_text = run(["./bin/python", "-I", "-m", "pip", "install", "--help"],
                        "PIP_CAPABILITY", cwd=work, pass_fds=(construction.fd,),
                        env=environment).stdout
        for option in ("--isolated", "--no-index", "--require-hashes", "--only-binary"):
            if option not in help_text:
                raise Failure("PIP_CAPABILITY_MISSING", "PIP_CAPABILITY")
        diagnostic_stage, diagnostic_operation = "OFFLINE_INSTALL", "INSTALL_OFFLINE"
        run(["./bin/python", "-I", "-m", "pip", "--isolated", "install", "--no-index",
             "--no-deps", "--require-hashes", "--only-binary=:all:", "--no-cache-dir",
             "--disable-pip-version-check", "--find-links", inputs,
             "-r", f"/proc/self/fd/{lock_fd}"], "OFFLINE_INSTALL", timeout=120,
            cwd=work, pass_fds=(construction.fd, snapshot.fd, lock_fd), env=environment)
        diagnostic_stage, diagnostic_operation = "DISTRIBUTION_VALIDATION", "VALIDATE_DISTRIBUTIONS"
        distributions = exact_distribution_set(pathlib.Path("./bin/python"), cwd=work,
                pass_fds=(construction.fd,), env=environment)
        validate_venv_symlinks(construction)
        diagnostic_stage, diagnostic_operation = "CONSTRUCTION_CONFIRMATION", "CONFIRM_CONSTRUCTION"
        revalidate_owned_directory(construction, "CONSTRUCTION_CONFIRMATION")
        state["CONSTRUCTION_CONFIRMED"] = "TRUE"
        snapshot_parent = snapshot.parent
        diagnostic_stage, diagnostic_operation = "INPUT_SNAPSHOT_CLEANUP", "CLEAN_SNAPSHOT"
        cleanup_owned_directory(snapshot, "INPUT_SNAPSHOT_CLEANUP")
        snapshot_parent.close(); snapshot = None
        diagnostic_stage, diagnostic_operation = "EVIDENCE_PUBLICATION", "PUBLISH_SUCCESS_EVIDENCE"
        evidence_root = open_tmp_root("EVIDENCE_ROOT")
        evidence = create_owned_child(evidence_root, "hioc-pe4-runtime-construct-", 0o700,
                                      "EVIDENCE_PUBLICATION")
        state["EVIDENCE_STATE"] = "CREATED"
        evidence_document = {"schema_version": "1.0", "action": "PE-4.0B.2a-D",
            "governance_commit": args.governance_commit, "result": "PASS",
            "error_code": "NONE", "failure_stage": "COMPLETE",
            "rollback_recommended": False, "construction_directory": str(construction.path),
            "environment_identity": VERSIONED_NAME, "wheel_sha256": WHEEL_SHA256,
            "lock_sha256": LOCK_SHA256, "installed_distributions": distributions,
            "input_snapshot_retained": False, "eligibility_state": "AWAITING_CONFIRMATION"}
        evidence_digest = publish_owned_json(evidence, "result.json", evidence_document,
                                             "EVIDENCE_PUBLICATION")
        state["EVIDENCE_STATE"] = "CONFIRMED"
        eligibility = {"schema_version": "1.0", "action": "PE-4.0B.2a-D",
            "governance_commit": args.governance_commit,
            "construction_directory": str(construction.path),
            "environment_identity": VERSIONED_NAME, "wheel_sha256": WHEEL_SHA256,
            "lock_sha256": LOCK_SHA256, "evidence_directory": str(evidence.path),
            "evidence_sha256": evidence_digest, "result": "PASS"}
        diagnostic_stage, diagnostic_operation = "ELIGIBILITY_PUBLICATION", "PUBLISH_ELIGIBILITY"
        publish_owned_json(construction, ACTION_D_ELIGIBILITY, eligibility,
                           "ACTION_D_ELIGIBILITY", mode=0o400)
        state["ACTION_D_ELIGIBILITY"] = "CONFIRMED"
        state["CONSTRUCTION_RETAINED"] = "TRUE"
        state["CLEANUP_STATE"] = "COMPLETE"
        _emit_state(state); terminal("PASS", "NONE", "COMPLETE", False, evidence.path)
        print(f"CONSTRUCTION_DIRECTORY={construction.path}")
        return 0
    except Failure as exc:
        primary_stage, primary_operation = diagnostic_stage, diagnostic_operation
        cleanup_failed = False
        if snapshot is not None:
            try:
                snapshot_parent = snapshot.parent
                cleanup_owned_directory(snapshot, "INPUT_SNAPSHOT_CLEANUP")
                snapshot_parent.close(); snapshot = None
            except Failure as cleanup_exc:
                cleanup_failed = True; state["INPUT_SNAPSHOT_RETAINED"] = "TRUE"
                state["CLEANUP_EXCEPTION_CLASS"], state["CLEANUP_ERRNO"] = _diagnostic_exception(cleanup_exc)
        if construction is not None:
            if state["CONSTRUCTION_CONFIRMED"] == "TRUE":
                state["CONSTRUCTION_RETAINED"] = "TRUE"
            else:
                try: cleanup_owned_directory(construction, "CONSTRUCTION_CLEANUP")
                except Failure as cleanup_exc:
                    cleanup_failed = True; state["CONSTRUCTION_RETAINED"] = "TRUE"
                    state["CLEANUP_EXCEPTION_CLASS"], state["CLEANUP_ERRNO"] = _diagnostic_exception(cleanup_exc)
        state["CLEANUP_STATE"] = "FAILED" if cleanup_failed else "COMPLETE"
        if governance_commit is not None:
            _publish_failure_evidence(governance_commit, state, primary_stage, primary_operation,
                                      exc, exc.code, exc.stage)
        _emit_state(state); terminal("FAIL", exc.code, exc.stage, exc.rollback,
                 evidence.path if evidence is not None else None)
        _emit_diagnostics(primary_stage, primary_operation, exc, state)
        return 1
    except Exception as exc:
        primary_stage, primary_operation = diagnostic_stage, diagnostic_operation
        cleanup_failed = False
        if snapshot is not None:
            try:
                snapshot_parent = snapshot.parent
                cleanup_owned_directory(snapshot, "INPUT_SNAPSHOT_CLEANUP")
                snapshot_parent.close(); snapshot = None
            except Exception as cleanup_exc:
                cleanup_failed = True; state["INPUT_SNAPSHOT_RETAINED"] = "TRUE"
                state["CLEANUP_EXCEPTION_CLASS"], state["CLEANUP_ERRNO"] = _diagnostic_exception(cleanup_exc)
        if construction is not None:
            if state["CONSTRUCTION_CONFIRMED"] == "TRUE":
                state["CONSTRUCTION_RETAINED"] = "TRUE"
            else:
                try: cleanup_owned_directory(construction, "CONSTRUCTION_CLEANUP")
                except Exception as cleanup_exc:
                    cleanup_failed = True; state["CONSTRUCTION_RETAINED"] = "TRUE"
                    state["CLEANUP_EXCEPTION_CLASS"], state["CLEANUP_ERRNO"] = _diagnostic_exception(cleanup_exc)
        state["CLEANUP_STATE"] = "FAILED" if cleanup_failed else "COMPLETE"
        if governance_commit is not None:
            _publish_failure_evidence(governance_commit, state, primary_stage, primary_operation,
                                      exc, "UNEXPECTED_ERROR", "UNEXPECTED")
        _emit_state(state); terminal("FAIL", "UNEXPECTED_ERROR", "UNEXPECTED", False,
                 evidence.path if evidence is not None else None)
        _emit_diagnostics(primary_stage, primary_operation, exc, state)
        return 1
    finally:
        os.umask(old_umask)
        for directory in (construction, environment_root, runtime_root, runtime_parent,
                          evidence, evidence_root):
            if directory is not None: directory.close()
        if lock_fd >= 0: os.close(lock_fd)


if __name__ == "__main__":
    raise SystemExit(main())
