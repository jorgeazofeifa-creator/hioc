#!/usr/bin/env python3
"""PE-4.0B.2a-D: descriptor-bound private venv construction and offline install."""

import argparse
import json
import os
import pathlib

from hioc_pe4_runtime_common import *


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
             "ACTION_D_ELIGIBILITY": "NOT_CONFIRMED", "CLEANUP_STATE": "NOT_REQUIRED"}
    construction = snapshot = evidence = None
    lock_fd = -1
    runtime_parent = runtime_root = environment_root = evidence_root = None
    old_umask = os.umask(0o027)
    try:
        verify_pi3()
        parser = argparse.ArgumentParser()
        parser.add_argument("--governance-commit", required=True)
        parser.add_argument("--transfer-directory", required=True)
        args = parser.parse_args()
        verify_repository(SOURCE, args.governance_commit, (
            "tools/hioc-pe4-runtime-construct.py", "tools/hioc_pe4_runtime_common.py",
            "requirements-pe4.lock"))
        snapshot = create_action_d_input_snapshot(args.transfer_directory)
        state["INPUT_SNAPSHOT_CREATED"] = "TRUE"
        lock_size = os.stat("requirements-pe4.lock", dir_fd=snapshot.fd,
                            follow_symlinks=False).st_size
        lock_fd = sealed_snapshot_file(snapshot, "requirements-pe4.lock", lock_size, LOCK_SHA256)
        runtime_parent = open_trusted_owned_parent(RUNTIME_ROOT.parent, "ENVIRONMENT_ROOT")
        runtime_root = open_owned_directory(RUNTIME_ROOT, 0o750, "ENVIRONMENT_ROOT",
                                            parent=runtime_parent)
        environment_root = open_owned_directory(ENVIRONMENT_ROOT, 0o750,
                                                "ENVIRONMENT_ROOT", parent=runtime_root)
        construction = create_owned_child(environment_root,
            f".construct-{VERSIONED_NAME}-", 0o750, "CONSTRUCTION_CREATION")
        state["CONSTRUCTION_CREATED"] = "TRUE"
        environment = action_d_subprocess_environment()
        work = f"/proc/self/fd/{construction.fd}"
        inputs = f"/proc/self/fd/{snapshot.fd}"
        run(["/usr/bin/python3", "-I", "-m", "venv", "--copies", "."],
            "VENV_CREATION", timeout=120, cwd=work, pass_fds=(construction.fd,), env=environment)
        os.fchmod(construction.fd, 0o750)
        revalidate_owned_directory(construction, "VENV_FILESYSTEM")
        validate_venv_symlinks(construction)
        _runtime_probe(construction, environment)
        help_text = run(["./bin/python", "-I", "-m", "pip", "install", "--help"],
                        "PIP_CAPABILITY", cwd=work, pass_fds=(construction.fd,),
                        env=environment).stdout
        for option in ("--isolated", "--no-index", "--require-hashes", "--only-binary"):
            if option not in help_text:
                raise Failure("PIP_CAPABILITY_MISSING", "PIP_CAPABILITY")
        run(["./bin/python", "-I", "-m", "pip", "--isolated", "install", "--no-index",
             "--no-deps", "--require-hashes", "--only-binary=:all:", "--no-cache-dir",
             "--disable-pip-version-check", "--find-links", inputs,
             "-r", f"/proc/self/fd/{lock_fd}"], "OFFLINE_INSTALL", timeout=120,
            cwd=work, pass_fds=(construction.fd, snapshot.fd, lock_fd), env=environment)
        distributions = exact_distribution_set(pathlib.Path("./bin/python"), cwd=work,
                pass_fds=(construction.fd,), env=environment)
        validate_venv_symlinks(construction)
        revalidate_owned_directory(construction, "CONSTRUCTION_CONFIRMATION")
        state["CONSTRUCTION_CONFIRMED"] = "TRUE"
        snapshot_parent = snapshot.parent
        cleanup_owned_directory(snapshot, "INPUT_SNAPSHOT_CLEANUP")
        snapshot_parent.close(); snapshot = None
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
        publish_owned_json(construction, ACTION_D_ELIGIBILITY, eligibility,
                           "ACTION_D_ELIGIBILITY", mode=0o400)
        state["ACTION_D_ELIGIBILITY"] = "CONFIRMED"
        state["CONSTRUCTION_RETAINED"] = "TRUE"
        state["CLEANUP_STATE"] = "COMPLETE"
        _emit_state(state); terminal("PASS", "NONE", "COMPLETE", False, evidence.path)
        print(f"CONSTRUCTION_DIRECTORY={construction.path}")
        return 0
    except Failure as exc:
        cleanup_failed = False
        if snapshot is not None:
            try:
                snapshot_parent = snapshot.parent
                cleanup_owned_directory(snapshot, "INPUT_SNAPSHOT_CLEANUP")
                snapshot_parent.close(); snapshot = None
            except Failure:
                cleanup_failed = True; state["INPUT_SNAPSHOT_RETAINED"] = "TRUE"
        if construction is not None:
            if state["CONSTRUCTION_CONFIRMED"] == "TRUE":
                state["CONSTRUCTION_RETAINED"] = "TRUE"
            else:
                try: cleanup_owned_directory(construction, "CONSTRUCTION_CLEANUP")
                except Failure:
                    cleanup_failed = True; state["CONSTRUCTION_RETAINED"] = "TRUE"
        state["CLEANUP_STATE"] = "FAILED" if cleanup_failed else "COMPLETE"
        _emit_state(state); terminal("FAIL", exc.code, exc.stage, exc.rollback,
                 evidence.path if evidence is not None else None)
        return 1
    except Exception:
        cleanup_failed = False
        if snapshot is not None:
            try:
                snapshot_parent = snapshot.parent
                cleanup_owned_directory(snapshot, "INPUT_SNAPSHOT_CLEANUP")
                snapshot_parent.close(); snapshot = None
            except Exception:
                cleanup_failed = True; state["INPUT_SNAPSHOT_RETAINED"] = "TRUE"
        if construction is not None:
            if state["CONSTRUCTION_CONFIRMED"] == "TRUE":
                state["CONSTRUCTION_RETAINED"] = "TRUE"
            else:
                try: cleanup_owned_directory(construction, "CONSTRUCTION_CLEANUP")
                except Exception:
                    cleanup_failed = True; state["CONSTRUCTION_RETAINED"] = "TRUE"
        state["CLEANUP_STATE"] = "FAILED" if cleanup_failed else "COMPLETE"
        _emit_state(state); terminal("FAIL", "UNEXPECTED_ERROR", "UNEXPECTED", False,
                 evidence.path if evidence is not None else None)
        return 1
    finally:
        os.umask(old_umask)
        for directory in (construction, environment_root, runtime_root, runtime_parent,
                          evidence, evidence_root):
            if directory is not None: directory.close()
        if lock_fd >= 0: os.close(lock_fd)


if __name__ == "__main__":
    raise SystemExit(main())
