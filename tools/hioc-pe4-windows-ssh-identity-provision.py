#!/usr/bin/env python3
"""Provision the dedicated, noninteractive Windows identity required by PE-4 Action B."""
from __future__ import annotations

import base64
import getpass
import hashlib
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile

from hioc_pe4_runtime_common import (
    Failure, REPOSITORY_ROOT, SSH_IDENTITY_NAME, SSH_KEYGEN_SHA256,
    prepare_windows_hierarchy, run_bounded, secure_workstation_path, sha256,
    validate_workstation_path_acl, verify_repository, windows_openssh_tool,
    windows_path_entry_exists, windows_profile_root, windows_publish_no_replace,
    windows_reparse_point, workstation_cache_root,
)

ACTION = "PE4_WINDOWS_SSH_IDENTITY_PROVISION"
EXPECTED_OPERATOR = "JorgeAzofeifaCastill"
EXPECTED_PROFILE = pathlib.PureWindowsPath(r"C:\Users\JorgeAzofeifaCastill")
KEY_COMMENT = "hioc-pe4-action-b-windows"
KEY_TYPE = "ssh-ed25519"
STAGING_PREFIX = ".hioc-pe4-identity-stage-"
EVIDENCE_PREFIX = "identity-provision-evidence-"
STATE_KEYS = ("PRIVATE_KEY_ACL", "PUBLIC_KEY_ACL", "PRIVATE_KEY_PUBLIC_MATCH",
              "PUBLIC_KEY_PUBLISHED", "PRIVATE_KEY_PUBLISHED", "IDENTITY_CONFIRMED",
              "STAGING_CLEANUP", "EVIDENCE_DIRECTORY_CLEANUP", "EVIDENCE_PUBLISHED")


def initial_state() -> dict[str, str]:
    return {name: "FALSE" for name in STATE_KEYS}


def parse_cli(argv: list[str]) -> str:
    if len(argv) != 2 or argv[0] != "--governance-commit" or not re.fullmatch(r"[0-9a-f]{40}", argv[1]):
        raise Failure("INVALID_ARGUMENTS", "INPUT_VALIDATION")
    return argv[1]


def target_paths(*, profile_resolver=windows_profile_root,
                 operator_resolver=getpass.getuser,
                 reparse=windows_reparse_point) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    if os.name != "nt":
        raise Failure("WRONG_TARGET_OS", "TARGET_OS")
    if operator_resolver() != EXPECTED_OPERATOR:
        raise Failure("WRONG_WINDOWS_OPERATOR", "OPERATOR_IDENTITY")
    profile = profile_resolver()
    if pathlib.PureWindowsPath(str(profile)) != EXPECTED_PROFILE or not profile.is_absolute():
        raise Failure("UNSAFE_PROFILE_PATH", "PROFILE_PATH")
    if not profile.is_dir() or profile.is_symlink() or reparse(profile):
        raise Failure("REPARSE_TRAVERSAL", "PROFILE_PATH")
    ssh = profile / ".ssh"
    if ssh.parent != profile or not ssh.is_dir() or ssh.is_symlink() or reparse(ssh):
        raise Failure("UNSAFE_SSH_PATH", "SSH_PATH")
    return ssh, ssh / SSH_IDENTITY_NAME, ssh / (SSH_IDENTITY_NAME + ".pub")


def collision_check(private: pathlib.Path, public: pathlib.Path, *,
                    entry_exists=windows_path_entry_exists) -> None:
    if entry_exists(private) or entry_exists(public):
        raise Failure("TARGET_COLLISION", "COLLISION_CHECK")


def governed_keygen(*, resolver=windows_openssh_tool) -> pathlib.Path:
    try:
        tool = resolver("ssh-keygen")
    except Failure:
        raise Failure("SSH_KEYGEN_MISSING", "SSH_KEYGEN_RESOLUTION")
    if sha256(tool) != SSH_KEYGEN_SHA256:
        raise Failure("SSH_KEYGEN_IDENTITY_MISMATCH", "SSH_KEYGEN_IDENTITY")
    return tool


def create_private_child(parent: pathlib.Path, prefix: str, *, acl=secure_workstation_path,
                         reparse=windows_reparse_point, created=None) -> pathlib.Path:
    path = pathlib.Path(tempfile.mkdtemp(prefix=prefix, dir=parent))
    if created is not None:
        created(path)
    if path.parent != parent or reparse(path) or not path.is_dir():
        raise Failure("REPARSE_TRAVERSAL", "STAGING_PATH")
    acl(path, True)
    return path


def parse_public(value: str) -> tuple[str, str, str]:
    if len(value.encode("utf-8")) > 4096 or "\r" in value:
        raise Failure("PUBLIC_KEY_INVALID", "KEY_VALIDATION")
    lines = value.splitlines()
    if len(lines) != 1:
        raise Failure("PUBLIC_KEY_INVALID", "KEY_VALIDATION")
    parts = lines[0].split(" ")
    if len(parts) != 3 or not all(parts):
        raise Failure("PUBLIC_KEY_INVALID", "KEY_VALIDATION")
    key_type, encoded, comment = parts
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except Exception:
        raise Failure("PUBLIC_KEY_INVALID", "KEY_VALIDATION")
    if not decoded or len(decoded) > 1024:
        raise Failure("PUBLIC_KEY_INVALID", "KEY_VALIDATION")
    return key_type, encoded, comment


def harden(path: pathlib.Path, label: str, *, acl=secure_workstation_path,
           acl_validate=validate_workstation_path_acl) -> None:
    try:
        acl(path, False)
    except Exception:
        raise Failure(f"{label}_ACL_APPLICATION_FAILED", f"{label}_ACL")
    try:
        acl_validate(path, False)
    except Exception:
        raise Failure(f"{label}_ACL_VALIDATION_FAILED", f"{label}_ACL")


def validate_pair(private: pathlib.Path, public: pathlib.Path, keygen: pathlib.Path, *,
                  runner=run_bounded, reparse=windows_reparse_point,
                  acl_validate=validate_workstation_path_acl) -> str:
    for path, code in ((private, "PRIVATE_KEY_MISSING"), (public, "PUBLIC_KEY_MISSING")):
        if not path.is_file() or path.is_symlink() or reparse(path) or path.stat().st_size <= 0:
            raise Failure(code, "KEY_VALIDATION")
        try: acl_validate(path, False)
        except Exception: raise Failure(code.replace("MISSING", "ACL_VALIDATION_FAILED"), "KEY_VALIDATION")
    key_type, encoded, comment = parse_public(public.read_text(encoding="ascii"))
    if key_type != KEY_TYPE:
        raise Failure("INVALID_KEY_ALGORITHM", "KEY_VALIDATION")
    if comment != KEY_COMMENT:
        raise Failure("PUBLIC_KEY_COMMENT_MISMATCH", "KEY_VALIDATION")
    derived = runner([str(keygen), "-y", "-f", str(private)], "PAIR_VALIDATION",
                     timeout=10, max_output=4096)
    derived_type, derived_encoded, _ = parse_public(derived.stdout.strip() + " derived")
    if (derived_type, derived_encoded) != (key_type, encoded):
        raise Failure("PRIVATE_PUBLIC_MISMATCH", "KEY_VALIDATION")
    fingerprint = runner([str(keygen), "-lf", str(public), "-E", "sha256"],
                         "FINGERPRINT", timeout=10, max_output=4096).stdout.strip()
    match = re.fullmatch(r"\d+ (SHA256:[A-Za-z0-9+/]+={0,2}) .+ \(ED25519\)", fingerprint)
    if not match or len(match.group(1)) > 100:
        raise Failure("FINGERPRINT_DERIVATION_FAILED", "FINGERPRINT")
    return match.group(1)


def write_evidence(directory: pathlib.Path, state: dict[str, str], fingerprint: str,
                   private: pathlib.Path, public: pathlib.Path, result: str, code: str,
                   stage: str, rollback: bool, *, acl=secure_workstation_path,
                   acl_validate=validate_workstation_path_acl,
                   reparse=windows_reparse_point,
                   entry_exists=windows_path_entry_exists,
                   publish=windows_publish_no_replace) -> None:
    published_state = dict(state)
    published_state["EVIDENCE_PUBLISHED"] = "TRUE"
    document = {"schema_version": "1.0", "action": ACTION, "algorithm": "ED25519",
                "private_key_path": str(private), "public_key_path": str(public),
                "public_key_fingerprint": fingerprint, "public_key_comment": KEY_COMMENT,
                **{key.lower(): value for key, value in published_state.items()}, "result": result,
                "error_code": code, "failure_stage": stage,
                "rollback_recommended": rollback}
    payload = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    expected = hashlib.sha256(payload).digest()
    temporary, final = directory / ".result.tmp", directory / "result.json"
    if entry_exists(final):
        raise Failure("EVIDENCE_FINAL_EXISTS", "EVIDENCE_PREPARATION")
    with temporary.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(payload.decode("utf-8"))
        handle.flush(); os.fsync(handle.fileno())
    acl(temporary, False)
    _confirm_evidence(temporary, payload, expected, acl_validate=acl_validate, reparse=reparse)
    try:
        publish(temporary, final)
    except OSError:
        try:
            _confirm_evidence(final, payload, expected, acl_validate=acl_validate, reparse=reparse)
            if entry_exists(temporary):
                raise Failure("EVIDENCE_TEMP_RETAINED", "EVIDENCE_CONFIRMATION")
        except Exception:
            raise Failure("EVIDENCE_RENAME_UNCERTAIN", "EVIDENCE_PUBLICATION")
        return
    _confirm_evidence(final, payload, expected, acl_validate=acl_validate, reparse=reparse)
    if entry_exists(temporary):
        raise Failure("EVIDENCE_TEMP_RETAINED", "EVIDENCE_CONFIRMATION")


def _confirm_evidence(path: pathlib.Path, payload: bytes, expected_digest: bytes, *,
                      acl_validate=validate_workstation_path_acl,
                      reparse=windows_reparse_point) -> None:
    if not path.is_file() or path.is_symlink() or reparse(path):
        raise Failure("EVIDENCE_FINAL_UNSAFE", "EVIDENCE_CONFIRMATION")
    try:
        with path.open("rb") as handle:
            actual = handle.read(len(payload) + 1)
    except OSError:
        raise Failure("EVIDENCE_REREAD_FAILED", "EVIDENCE_CONFIRMATION")
    if actual != payload or hashlib.sha256(actual).digest() != expected_digest:
        raise Failure("EVIDENCE_IDENTITY_MISMATCH", "EVIDENCE_CONFIRMATION")
    try:
        acl_validate(path, False)
    except Exception:
        raise Failure("EVIDENCE_ACL_INVALID", "EVIDENCE_CONFIRMATION")


def safe_cleanup(path: pathlib.Path, parent: pathlib.Path, prefix: str = STAGING_PREFIX, *,
                 reparse=windows_reparse_point) -> None:
    suffix = path.name[len(prefix):] if path.name.startswith(prefix) else ""
    if path.parent != parent or path == parent or not re.fullmatch(r"[a-z0-9_]{8}", suffix) or reparse(path):
        raise Failure("CLEANUP_PATH_INVALID", "CLEANUP")
    for item in path.iterdir():
        if item.is_dir() or item.is_symlink() or reparse(item):
            raise Failure("CLEANUP_CONTENT_UNSAFE", "CLEANUP")
    shutil.rmtree(path)


def evidence_root(*, resolver=workstation_cache_root, acl=secure_workstation_path,
                  reparse=windows_reparse_point) -> pathlib.Path:
    root = resolver()
    trusted = root.parents[2]
    if root != trusted / "HIOC/artifacts/pe4":
        raise Failure("WORKSTATION_PATH_INVALID", "EVIDENCE_PATH")
    hioc = prepare_windows_hierarchy(trusted, ("HIOC",), acl=acl, reparse=reparse)
    pe4 = prepare_windows_hierarchy(hioc, ("artifacts", "pe4"), acl=acl, reparse=reparse)
    return prepare_windows_hierarchy(pe4, ("evidence",), acl=acl, reparse=reparse)


def terminal_lines(state: dict[str, str], result: str, code: str, stage: str,
                   rollback: bool, fingerprint: str, evidence: pathlib.Path | None) -> list[str]:
    lines = [f"{key}={state[key]}" for key in STATE_KEYS]
    lines += ["ACTION_B=BLOCKED", f"RESULT={result}", f"ERROR_CODE={code}",
              f"FAILURE_STAGE={stage}", f"ROLLBACK_RECOMMENDED={'TRUE' if rollback else 'FALSE'}"]
    if fingerprint: lines.append(f"PUBLIC_KEY_FINGERPRINT={fingerprint}")
    if evidence is not None: lines.append(f"EVIDENCE_DIR={evidence}")
    return lines


def execute(governance_commit: str, *, runner=run_bounded, acl=secure_workstation_path,
            acl_validate=validate_workstation_path_acl, reparse=windows_reparse_point,
            profile_resolver=windows_profile_root, operator_resolver=getpass.getuser,
            keygen_resolver=windows_openssh_tool, evidence_resolver=workstation_cache_root,
            evidence_writer=write_evidence, entry_exists=windows_path_entry_exists,
            publish=windows_publish_no_replace) -> tuple[list[str], int]:
    state, staging, evidence, fingerprint = initial_state(), None, None, ""
    children: dict[str, pathlib.Path] = {}
    evidence_ready = evidence_attempted = False
    private = public = pathlib.Path("UNAVAILABLE")
    primary: Failure | None = None
    try:
        verify_repository(REPOSITORY_ROOT, governance_commit,
                          ("tools/hioc-pe4-windows-ssh-identity-provision.py",
                           "tools/hioc_pe4_runtime_common.py"))
        ssh, private, public = target_paths(profile_resolver=profile_resolver,
                                             operator_resolver=operator_resolver, reparse=reparse)
        collision_check(private, public, entry_exists=entry_exists)
        keygen = governed_keygen(resolver=keygen_resolver)
        root = evidence_root(resolver=evidence_resolver, acl=acl, reparse=reparse)
        evidence = create_private_child(root, EVIDENCE_PREFIX, acl=acl, reparse=reparse,
                                        created=lambda path: children.__setitem__("evidence", path))
        evidence_ready = True
        staging = create_private_child(ssh, STAGING_PREFIX, acl=acl, reparse=reparse,
                                       created=lambda path: children.__setitem__("staging", path))
        collision_check(private, public, entry_exists=entry_exists)
        staged_private, staged_public = staging / SSH_IDENTITY_NAME, staging / (SSH_IDENTITY_NAME + ".pub")
        try:
            runner([str(keygen), "-q", "-t", "ed25519", "-N", "", "-C", KEY_COMMENT,
                    "-f", str(staged_private)], "KEY_GENERATION", timeout=20, max_output=4096)
        except Failure:
            raise Failure("GENERATION_FAILED", "KEY_GENERATION")
        if set(staging.iterdir()) != {staged_private, staged_public}:
            raise Failure("UNEXPECTED_GENERATION_OUTPUT", "STAGING_VALIDATION")
        harden(staged_private, "PRIVATE_KEY", acl=acl, acl_validate=acl_validate); state["PRIVATE_KEY_ACL"] = "PASS"
        harden(staged_public, "PUBLIC_KEY", acl=acl, acl_validate=acl_validate); state["PUBLIC_KEY_ACL"] = "PASS"
        fingerprint = validate_pair(staged_private, staged_public, keygen, runner=runner,
                                    reparse=reparse, acl_validate=acl_validate)
        state["PRIVATE_KEY_PUBLIC_MATCH"] = "PASS"
        collision_check(private, public, entry_exists=entry_exists)
        try: publish(staged_public, public)
        except OSError:
            if public.is_file() and not public.is_symlink() and not reparse(public) and not staged_public.exists():
                if validate_pair(staged_private, public, keygen, runner=runner, reparse=reparse,
                                 acl_validate=acl_validate) == fingerprint:
                    state["PUBLIC_KEY_PUBLISHED"] = "TRUE"
            raise Failure("PUBLIC_KEY_PUBLICATION_FAILED", "PUBLIC_KEY_PUBLICATION", state["PUBLIC_KEY_PUBLISHED"] == "TRUE")
        state["PUBLIC_KEY_PUBLISHED"] = "TRUE"
        if entry_exists(private):
            raise Failure("TARGET_COLLISION", "COLLISION_CHECK")
        try: publish(staged_private, private)
        except OSError:
            if private.is_file() and not private.is_symlink() and not reparse(private) and not staged_private.exists():
                if validate_pair(private, public, keygen, runner=runner, reparse=reparse,
                                 acl_validate=acl_validate) == fingerprint:
                    state["PRIVATE_KEY_PUBLISHED"] = "TRUE"
            raise Failure("PRIVATE_KEY_PUBLICATION_FAILED", "PRIVATE_KEY_PUBLICATION", state["PRIVATE_KEY_PUBLISHED"] == "TRUE")
        state["PRIVATE_KEY_PUBLISHED"] = "TRUE"
        harden(public, "PUBLIC_KEY", acl=acl, acl_validate=acl_validate)
        harden(private, "PRIVATE_KEY", acl=acl, acl_validate=acl_validate)
        confirmed = validate_pair(private, public, keygen, runner=runner, reparse=reparse,
                                  acl_validate=acl_validate)
        if confirmed != fingerprint: raise Failure("FINAL_IDENTITY_CONFIRMATION_FAILED", "FINAL_CONFIRMATION", True)
        state["IDENTITY_CONFIRMED"] = "TRUE"
        try: safe_cleanup(staging, ssh, STAGING_PREFIX, reparse=reparse)
        except Exception: raise Failure("STAGING_CLEANUP_FAILED", "CLEANUP", True)
        state["STAGING_CLEANUP"] = "PASS"; staging = None
        evidence_attempted = True
        try:
            evidence_writer(evidence, state, fingerprint, private, public, "PASS", "NONE",
                            "COMPLETE", False, acl=acl, acl_validate=acl_validate,
                            reparse=reparse, entry_exists=entry_exists, publish=publish)
        except Exception:
            raise Failure("EVIDENCE_PUBLICATION_FAILED", "EVIDENCE_PUBLICATION", True)
        state["EVIDENCE_PUBLISHED"] = "TRUE"
        return terminal_lines(state, "PASS", "NONE", "COMPLETE", False, fingerprint, evidence), 0
    except Failure as failure: primary = failure
    except Exception: primary = Failure("UNEXPECTED_ERROR", "UNEXPECTED", state["PRIVATE_KEY_PUBLISHED"] == "TRUE")
    assert primary is not None
    rollback = primary.rollback or state["PUBLIC_KEY_PUBLISHED"] == "TRUE" or state["PRIVATE_KEY_PUBLISHED"] == "TRUE"
    staging = staging or children.get("staging")
    evidence = evidence or children.get("evidence")
    if staging is not None and state["PUBLIC_KEY_PUBLISHED"] == "FALSE" and state["PRIVATE_KEY_PUBLISHED"] == "FALSE":
        try:
            safe_cleanup(staging, staging.parent, STAGING_PREFIX, reparse=reparse)
            state["STAGING_CLEANUP"] = "PASS"
            staging = None
        except Exception:
            state["STAGING_CLEANUP"] = "FAILED"
    if evidence is not None and not evidence_ready:
        try:
            safe_cleanup(evidence, evidence.parent, EVIDENCE_PREFIX, reparse=reparse)
            state["EVIDENCE_DIRECTORY_CLEANUP"] = "PASS"
            evidence = None
        except Exception:
            state["EVIDENCE_DIRECTORY_CLEANUP"] = "FAILED"
    if evidence_ready and evidence is not None and not evidence_attempted:
        evidence_attempted = True
        try:
            evidence_writer(evidence, state, fingerprint, private, public, "FAIL", primary.code,
                            primary.stage, rollback, acl=acl, acl_validate=acl_validate,
                            reparse=reparse, entry_exists=entry_exists, publish=publish)
            state["EVIDENCE_PUBLISHED"] = "TRUE"
        except Exception:
            state["EVIDENCE_PUBLISHED"] = "FALSE"
    return terminal_lines(state, "FAIL", primary.code, primary.stage, rollback, fingerprint, evidence), 1


def main(argv: list[str]) -> int:
    try: commit = parse_cli(argv)
    except Failure:
        print("\n".join(terminal_lines(initial_state(), "FAIL", "INVALID_ARGUMENTS", "INPUT_VALIDATION", False, "", None)))
        return 1
    lines, status = execute(commit); print("\n".join(lines)); return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
