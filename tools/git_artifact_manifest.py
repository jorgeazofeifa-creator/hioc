#!/usr/bin/env python3
"""Derive deployment artifact identity from exact Git objects."""

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys


def git(repo, *args, binary=False):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def build_manifest(repo, revision, paths, compare_worktree=False):
    commit = git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}")
    artifacts = []
    for path_text in paths:
        path = pathlib.PurePosixPath(path_text)
        if path.is_absolute() or ".." in path.parts or str(path) in ("", "."):
            raise ValueError(f"invalid repository-relative path: {path_text}")
        tree_entry = git(repo, "ls-tree", commit, "--", str(path))
        fields = tree_entry.split(None, 3)
        if len(fields) != 4 or fields[1] != "blob" or fields[3].split("\t", 1)[-1] != str(path):
            raise ValueError(f"path is not a regular Git blob at {commit}: {path}")
        mode, _, blob, _ = fields
        raw = git(repo, "cat-file", "blob", blob, binary=True)
        artifact = {
            "path": str(path),
            "git_blob": blob,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "mode": mode,
        }
        if compare_worktree:
            worktree_path = pathlib.Path(repo, *path.parts)
            if not worktree_path.is_file():
                artifact["working_tree_equal"] = False
                artifact["working_tree_sha256"] = None
            else:
                worktree = worktree_path.read_bytes()
                artifact["working_tree_equal"] = worktree == raw
                artifact["working_tree_sha256"] = hashlib.sha256(worktree).hexdigest()
        artifacts.append(artifact)
    return {
        "schema_version": 1,
        "commit": commit,
        "generated_from_git_objects": True,
        "artifacts": artifacts,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit", help="exact approved commit SHA")
    parser.add_argument("paths", nargs="+", help="repository-relative artifact paths")
    parser.add_argument("--repo", default=".", help="Git repository")
    parser.add_argument("--compare-worktree", action="store_true")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()
    try:
        manifest = build_manifest(args.repo, args.commit, args.paths, args.compare_worktree)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(manifest, indent=2, sort_keys=True))
    else:
        print(f"Commit: {manifest['commit']}")
        for item in manifest["artifacts"]:
            print(f"Path: {item['path']}")
            print(f"Git blob: {item['git_blob']}")
            print(f"Git-derived SHA-256: {item['sha256']}")
            print(f"Size: {item['size_bytes']} bytes")
            print(f"Mode: {item['mode']}")
            if "working_tree_equal" in item:
                print(f"Working-tree equal: {str(item['working_tree_equal']).lower()}")
                print(f"Working-tree SHA-256: {item['working_tree_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
