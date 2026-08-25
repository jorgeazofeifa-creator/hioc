#!/usr/bin/env python3
"""PE-4.0B.2a-A: bounded Windows acquisition of the exact governed wheel."""
from __future__ import annotations

import hashlib
import http.client
import json
import os
import pathlib
import re
import shutil
import ssl
import sys
import tempfile
import time
import urllib.parse

from hioc_pe4_runtime_common import (
    Failure, REPOSITORY_ROOT, WHEEL_NAME, WHEEL_SHA256, WHEEL_SIZE, WHEEL_URL,
    prepare_windows_hierarchy, secure_workstation_path, verify_repository,
    windows_reparse_point, workstation_cache_root,
)

TOTAL_DEADLINE_SECONDS = 20.0
MAX_RESPONSE_BYTES = WHEEL_SIZE + 1
HIOC_PARTS = ("HIOC",)
PE4_PARTS = ("artifacts", "pe4")
CACHE_PARTS = ("cache",)
STAGING_PARTS = ("staging",)
EVIDENCE_PARTS = ("evidence",)
STAGING_PREFIX = "action-a-stage-"
EVIDENCE_PREFIX = "action-a-evidence-"
STATE_KEYS = ("ARTIFACT_ACQUIRED", "ARTIFACT_VERIFIED", "DURABLE_CACHE_PUBLISHED",
              "CACHE_REUSED", "EVIDENCE_PUBLISHED")


def initial_state() -> dict[str, str]:
    return {key: "FALSE" for key in STATE_KEYS}


def parse_cli(argv: list[str]) -> str:
    if len(argv) != 2 or argv[0] != "--governance-commit" or not re.fullmatch(r"[0-9a-f]{40}", argv[1]):
        raise Failure("INVALID_ARGUMENTS", "INPUT_VALIDATION")
    return argv[1]


def roots(*, cache_resolver=workstation_cache_root, acl=secure_workstation_path,
          reparse=windows_reparse_point) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    legacy = cache_resolver()
    trusted = legacy.parents[2]
    if legacy != trusted / "HIOC/artifacts/pe4":
        raise Failure("WORKSTATION_PATH_INVALID", "WORKSTATION_PATH")
    hioc = prepare_windows_hierarchy(trusted, HIOC_PARTS, acl=acl, reparse=reparse)
    pe4 = prepare_windows_hierarchy(hioc, PE4_PARTS, acl=acl, reparse=reparse)
    cache = prepare_windows_hierarchy(pe4, CACHE_PARTS, acl=acl, reparse=reparse)
    staging = prepare_windows_hierarchy(pe4, STAGING_PARTS, acl=acl, reparse=reparse)
    evidence = prepare_windows_hierarchy(pe4, EVIDENCE_PARTS, acl=acl, reparse=reparse)
    return cache, staging, evidence


def private_child(parent: pathlib.Path, prefix: str, *, acl=secure_workstation_path) -> pathlib.Path:
    child = pathlib.Path(tempfile.mkdtemp(prefix=prefix, dir=parent))
    acl(child, True)
    return child


def remaining(deadline: float, clock) -> float:
    value = deadline - clock()
    if value <= 0:
        raise Failure("ACQUISITION_DEADLINE_EXCEEDED", "ACQUISITION")
    return value


def download(*, connection_factory=http.client.HTTPSConnection, clock=time.monotonic) -> bytes:
    parsed = urllib.parse.urlsplit(WHEEL_URL)
    if parsed.scheme != "https" or parsed.hostname != "files.pythonhosted.org" or parsed.query or parsed.fragment:
        raise Failure("ARTIFACT_ENDPOINT_INVALID", "ACQUISITION")
    deadline = clock() + TOTAL_DEADLINE_SECONDS
    context = ssl.create_default_context()
    connection = connection_factory(parsed.hostname, timeout=remaining(deadline, clock), context=context)
    try:
        connection.request("GET", parsed.path, headers={"User-Agent": "HIOC-PE4-artifact/1", "Connection": "close"})
        if getattr(connection, "sock", None) is not None:
            connection.sock.settimeout(remaining(deadline, clock))
        response = connection.getresponse()
        if response.status != 200:
            code = "ARTIFACT_REDIRECT_REFUSED" if 300 <= response.status < 400 else "ARTIFACT_RESPONSE_INVALID"
            raise Failure(code, "ACQUISITION")
        if response.getheader("Content-Length") != str(WHEEL_SIZE):
            raise Failure("ARTIFACT_RESPONSE_INVALID", "ACQUISITION")
        chunks, total = [], 0
        while True:
            budget = remaining(deadline, clock)
            if getattr(connection, "sock", None) is not None:
                connection.sock.settimeout(budget)
            block = response.read(min(65536, MAX_RESPONSE_BYTES - total))
            if not block: break
            chunks.append(block); total += len(block)
            if total >= MAX_RESPONSE_BYTES:
                raise Failure("ARTIFACT_RESPONSE_TOO_LARGE", "ACQUISITION")
        if total != WHEEL_SIZE:
            raise Failure("ARTIFACT_SIZE_MISMATCH", "ACQUISITION")
        return b"".join(chunks)
    except TimeoutError:
        raise Failure("ACQUISITION_DEADLINE_EXCEEDED", "ACQUISITION")
    finally:
        connection.close()


def validate_payload(data: bytes) -> None:
    if len(data) != WHEEL_SIZE:
        raise Failure("ARTIFACT_SIZE_MISMATCH", "ARTIFACT_IDENTITY")
    if hashlib.sha256(data).hexdigest() != WHEEL_SHA256:
        raise Failure("ARTIFACT_SHA256_MISMATCH", "ARTIFACT_IDENTITY")


def safe_remove_invocation(path: pathlib.Path, parent: pathlib.Path, prefix: str,
                           *, reparse=windows_reparse_point) -> None:
    suffix = path.name[len(prefix):] if path.name.startswith(prefix) else ""
    if (path.parent != parent or not re.fullmatch(r"[a-z0-9_]{8}", suffix)
            or path == parent or reparse(path)):
        raise Failure("CLEANUP_PATH_INVALID", "CLEANUP")
    def check(directory: pathlib.Path) -> None:
        for item in directory.iterdir():
            if reparse(item): raise Failure("CLEANUP_REPARSE_POINT", "CLEANUP")
            if item.is_dir(): check(item)
    check(path)
    shutil.rmtree(path)


def publish_cache(data: bytes, stage: pathlib.Path, cache: pathlib.Path,
                  *, acl=secure_workstation_path, published=None) -> bool:
    temporary = stage / WHEEL_NAME
    with temporary.open("xb") as handle:
        handle.write(data); handle.flush(); os.fsync(handle.fileno())
    acl(temporary, False)
    validate_payload(temporary.read_bytes())
    durable = cache / WHEEL_NAME
    if durable.exists() or durable.is_symlink():
        if durable.is_symlink() or not durable.is_file():
            raise Failure("DURABLE_CACHE_CONFLICT", "CACHE_PUBLICATION")
        existing = durable.read_bytes()
        if len(existing) != WHEEL_SIZE or hashlib.sha256(existing).hexdigest() != WHEEL_SHA256:
            raise Failure("DURABLE_CACHE_CONFLICT", "CACHE_PUBLICATION")
        acl(durable, False)
        temporary.unlink()
        return True
    os.replace(temporary, durable)
    if published is not None: published()
    acl(durable, False)
    existing = durable.read_bytes()
    if len(existing) != WHEEL_SIZE or hashlib.sha256(existing).hexdigest() != WHEEL_SHA256:
        raise Failure("DURABLE_CACHE_PUBLICATION_FAILED", "CACHE_PUBLICATION")
    return False


def write_windows_evidence(directory: pathlib.Path, state: dict[str, str], result: str,
                           code: str, stage: str, *, acl=secure_workstation_path,
                           replace=os.replace) -> None:
    document = {"schema_version": "1.0", "action": "PE-4.0B.2a-A",
                "artifact_filename": WHEEL_NAME, "artifact_size": WHEEL_SIZE,
                "approved_sha256": WHEEL_SHA256,
                **{key.lower(): state[key] for key in STATE_KEYS}, "result": result,
                "error_code": code, "failure_stage": stage, "rollback_recommended": False}
    temporary = directory / ".result.tmp"
    with temporary.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, sort_keys=True, separators=(",", ":")); handle.write("\n")
        handle.flush(); os.fsync(handle.fileno())
    acl(temporary, False)
    replace(temporary, directory / "result.json")
    acl(directory / "result.json", False)


def terminal_lines(state: dict[str, str], result: str, code: str, stage: str,
                   evidence: pathlib.Path | None) -> list[str]:
    lines = [f"{key}={state[key]}" for key in STATE_KEYS]
    lines.append(f"ACTION_A={'COMPLETE' if result == 'PASS' else 'NOT_COMPLETE'}")
    lines += [f"RESULT={result}", f"ERROR_CODE={code}", f"FAILURE_STAGE={stage}",
              "ROLLBACK_RECOMMENDED=FALSE"]
    if evidence is not None: lines.append(f"EVIDENCE_DIR={evidence}")
    return lines


def execute(governance_commit: str, *, connection_factory=http.client.HTTPSConnection,
            clock=time.monotonic, cache_resolver=workstation_cache_root,
            acl=secure_workstation_path, reparse=windows_reparse_point,
            evidence_writer=write_windows_evidence) -> tuple[list[str], int]:
    state, evidence_dir, stage_dir = initial_state(), None, None
    try:
        verify_repository(REPOSITORY_ROOT, governance_commit,
                          ("tools/hioc-pe4-artifact-acquire.py", "tools/hioc_pe4_runtime_common.py", "requirements-pe4.lock"))
        cache, staging, evidence_root = roots(cache_resolver=cache_resolver, acl=acl, reparse=reparse)
        evidence_dir = private_child(evidence_root, EVIDENCE_PREFIX, acl=acl)
        stage_dir = private_child(staging, STAGING_PREFIX, acl=acl)
        data = download(connection_factory=connection_factory, clock=clock); state["ARTIFACT_ACQUIRED"] = "TRUE"
        validate_payload(data); state["ARTIFACT_VERIFIED"] = "TRUE"
        reused = publish_cache(data, stage_dir, cache, acl=acl,
                               published=lambda: state.__setitem__("DURABLE_CACHE_PUBLISHED", "TRUE"))
        state["DURABLE_CACHE_PUBLISHED"] = "TRUE"; state["CACHE_REUSED"] = "TRUE" if reused else "FALSE"
        safe_remove_invocation(stage_dir, staging, STAGING_PREFIX, reparse=reparse); stage_dir = None
        state["EVIDENCE_PUBLISHED"] = "TRUE"
        try: evidence_writer(evidence_dir, state, "PASS", "NONE", "COMPLETE", acl=acl)
        except Exception:
            state["EVIDENCE_PUBLISHED"] = "FALSE"
            raise Failure("EVIDENCE_PUBLICATION_FAILED", "EVIDENCE_PUBLICATION")
        return terminal_lines(state, "PASS", "NONE", "COMPLETE", evidence_dir), 0
    except Failure as failure:
        code, stage = failure.code, failure.stage
    except Exception:
        code, stage = "UNEXPECTED_ERROR", "UNEXPECTED"
    if evidence_dir is not None and state["EVIDENCE_PUBLISHED"] == "FALSE":
        try:
            state["EVIDENCE_PUBLISHED"] = "TRUE"
            evidence_writer(evidence_dir, state, "FAIL", code, stage, acl=acl)
        except Exception:
            state["EVIDENCE_PUBLISHED"] = "FALSE"
            code, stage = "EVIDENCE_PUBLICATION_FAILED", "EVIDENCE_PUBLICATION"
    if stage_dir is not None:
        try: safe_remove_invocation(stage_dir, stage_dir.parent, STAGING_PREFIX, reparse=reparse)
        except Exception: code, stage = "STAGING_CLEANUP_FAILED", "CLEANUP"
    return terminal_lines(state, "FAIL", code, stage, evidence_dir), 1


def main(argv: list[str]) -> int:
    try: commit = parse_cli(argv)
    except Failure:
        print("\n".join(terminal_lines(initial_state(), "FAIL", "INVALID_ARGUMENTS", "INPUT_VALIDATION", None)))
        return 1
    lines, status = execute(commit); print("\n".join(lines)); return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
