#!/usr/bin/env python3
"""Fail-closed Git provenance and current-source gates for handoff consumers."""

import pathlib
import re
import subprocess

from hioc_pe4_runtime_common import Failure

CRITICAL_PRODUCER_PATHS = (
    "tools/hioc-pe4-runtime-construct.py",
    "tools/hioc_pe4_runtime_common.py",
    "requirements-pe4.lock",
)
CURRENT_CONSUMER_PATHS = (
    "tools/hioc-pe4-dependency-validate.py",
    "tools/hioc_pe4_handoff_compatibility.py",
    *CRITICAL_PRODUCER_PATHS,
)
ACTIVE_OPERATIONS = (
    "MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD",
    "rebase-merge", "rebase-apply", "sequencer", "BISECT_START",
)


def _git(root, arguments, stage):
    # Apply to every command, including object reads, ancestry and ref checks.
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), *arguments],
            capture_output=True, text=True, encoding="utf-8", errors="strict",
            timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError, UnicodeError):
        raise Failure("HANDOFF_GIT_FAILED", stage) from None
    if result.returncode != 0:
        raise Failure("HANDOFF_GIT_FAILED", stage)
    return result.stdout.strip()


def validate_commit_id(value, stage):
    """Validate literal syntax; object existence/type is a separate Git gate."""
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise Failure("INVALID_GOVERNANCE_COMMIT", stage)


def _commit(root, value, stage):
    validate_commit_id(value, stage)
    if _git(root, ["cat-file", "-t", value], stage) != "commit":
        raise Failure("HANDOFF_COMMIT_OBJECT_INVALID", stage)


def _blob(root, commit, relative, stage):
    oid = _git(root, ["rev-parse", "--verify", f"{commit}:{relative}"], stage)
    if re.fullmatch(r"[0-9a-f]{40}", oid) is None or _git(
            root, ["cat-file", "-t", oid], stage) != "blob":
        raise Failure("HANDOFF_BLOB_OBJECT_INVALID", stage)
    return oid


def verify_handoff_compatibility(root, producer_commit, consumer_commit):
    """Require complete history, producer ancestry and identical upstream blobs."""
    stage = "HANDOFF_COMPATIBILITY"
    _commit(root, producer_commit, stage)
    _commit(root, consumer_commit, stage)
    if _git(root, ["rev-parse", "--is-shallow-repository"], stage) != "false":
        raise Failure("HANDOFF_HISTORY_INCOMPLETE", stage)
    # merge-base exit 1 (nonancestor) and command errors both fail closed.
    _git(root, ["merge-base", "--is-ancestor", producer_commit, consumer_commit], stage)
    for relative in CRITICAL_PRODUCER_PATHS:
        if _blob(root, producer_commit, relative, stage) != _blob(
                root, consumer_commit, relative, stage):
            raise Failure("HANDOFF_CRITICAL_BLOB_MISMATCH", stage)


def verify_current_consumer_source(root, consumer_commit):
    """Bind the clean main checkout and normalized source to the consumer."""
    root = pathlib.Path(root)
    stage = "SOURCE_IDENTITY"
    _commit(root, consumer_commit, stage)
    for arguments, expected in (
        (["branch", "--show-current"], "main"),
        (["rev-parse", "--verify", "HEAD"], consumer_commit),
        (["rev-parse", "--verify", "refs/remotes/origin/main"], consumer_commit),
    ):
        if _git(root, arguments, stage) != expected:
            raise Failure("SOURCE_IDENTITY_MISMATCH", stage)
    if _git(root, ["rev-list", "--left-right", "--count",
                   "HEAD...refs/remotes/origin/main"], stage).split() != ["0", "0"]:
        raise Failure("SOURCE_IDENTITY_MISMATCH", stage)
    for name in ACTIVE_OPERATIONS:
        location = pathlib.Path(_git(root, ["rev-parse", "--git-path", name], stage))
        if not location.is_absolute():
            location = root / location
        if location.exists() or location.is_symlink():
            raise Failure("SOURCE_GIT_OPERATION_ACTIVE", stage)
    if _git(root, ["status", "--porcelain", "--untracked-files=all"], stage):
        raise Failure("SOURCE_REPOSITORY_DIRTY", stage)
    for relative in CURRENT_CONSUMER_PATHS:
        expected = _blob(root, consumer_commit, relative, stage)
        actual = _git(root, ["hash-object", "--path", relative,
                             str(root / relative)], stage)
        if actual != expected:
            raise Failure("SOURCE_WORKTREE_IDENTITY_MISMATCH", stage)
