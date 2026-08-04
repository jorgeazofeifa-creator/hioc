#!/usr/bin/env python3
"""Validate PE-2 Git content identity separately from runtime permissions."""

import argparse
import hashlib
import json
import pathlib
try:
    import pwd
    import grp
except ImportError:  # Repository-host portability; production is Linux.
    pwd = grp = None
import stat
import sys


class ValidationFailure(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def load_json(path):
    with pathlib.Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate(manifest, git_manifest, runtime_root, owner_lookup=None, group_lookup=None, mode_lookup=None):
    expected_keys = {"schema_version", "owner", "group", "artifacts"}
    if not isinstance(manifest, dict) or set(manifest) != expected_keys or manifest["schema_version"] != "1.0":
        raise ValidationFailure("RUNTIME_PERMISSION_CONTRACT_INVALID", "runtime permission contract is invalid")
    by_path = {item["path"]: item for item in git_manifest.get("artifacts", [])}
    results = []
    if owner_lookup is None:
        if pwd is None:
            raise ValidationFailure("VALIDATOR_INTERNAL_ERROR", "owner lookup is unavailable")
        owner_lookup = lambda uid: pwd.getpwuid(uid).pw_name
    if group_lookup is None:
        if grp is None:
            raise ValidationFailure("VALIDATOR_INTERNAL_ERROR", "group lookup is unavailable")
        group_lookup = lambda gid: grp.getgrgid(gid).gr_name
    mode_lookup = mode_lookup or (lambda info: stat.S_IMODE(info.st_mode))
    for policy in manifest["artifacts"]:
        if set(policy) != {"path", "runtime_mode", "executable", "privacy"}:
            raise ValidationFailure("RUNTIME_PERMISSION_CONTRACT_INVALID", "artifact permission entry is invalid")
        path_text = policy["path"]
        git_item = by_path.get(path_text)
        if git_item is None:
            raise ValidationFailure("RUNTIME_ARTIFACT_MISMATCH", "Git artifact manifest is incomplete")
        path = pathlib.Path(runtime_root) / pathlib.PurePosixPath(path_text)
        if path.is_symlink() or not path.is_file():
            raise ValidationFailure("RUNTIME_PERMISSION_MISMATCH", "runtime artifact is missing, non-regular, or a symlink")
        raw = path.read_bytes()
        runtime_sha = hashlib.sha256(raw).hexdigest()
        if runtime_sha != git_item["sha256"]:
            raise ValidationFailure("RUNTIME_ARTIFACT_MISMATCH", "runtime artifact bytes differ from approved Git object")
        info = path.stat()
        mode_value = mode_lookup(info)
        actual_mode = f"{mode_value:04o}"
        actual_owner, actual_group = owner_lookup(info.st_uid), group_lookup(info.st_gid)
        if actual_mode != policy["runtime_mode"]:
            raise ValidationFailure("RUNTIME_PERMISSION_MISMATCH", "runtime artifact mode differs from policy")
        if actual_owner != manifest["owner"] or actual_group != manifest["group"]:
            raise ValidationFailure("RUNTIME_OWNERSHIP_MISMATCH", "runtime artifact ownership differs from policy")
        executable = bool(mode_value & 0o100)
        if executable != policy["executable"]:
            raise ValidationFailure("RUNTIME_PERMISSION_MISMATCH", "runtime executable classification differs from policy")
        results.append({
            "path": path_text, "git_blob": git_item["git_blob"], "git_mode": git_item["mode"],
            "git_sha256": git_item["sha256"], "runtime_sha256": runtime_sha,
            "content_equal": True, "expected_runtime_mode": policy["runtime_mode"],
            "runtime_mode": actual_mode, "executable": executable,
            "owner": actual_owner, "group": actual_group, "privacy": policy["privacy"],
            "permission_equal": True,
        })
    return {"schema_version": "1.0", "artifact_identity": "PASS", "runtime_permissions": "PASS", "artifacts": results}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--git-manifest", required=True)
    parser.add_argument("--runtime-root", required=True)
    args = parser.parse_args(argv)
    try:
        result = validate(load_json(args.contract), load_json(args.git_manifest), pathlib.Path(args.runtime_root))
    except ValidationFailure as exc:
        print(json.dumps({"result": "FAIL", "error_code": exc.code, "error_message": exc.message}, sort_keys=True))
        return 1
    except Exception:
        print(json.dumps({"result": "VALIDATION_FAIL", "error_code": "VALIDATOR_INTERNAL_ERROR", "error_message": "artifact validator failed"}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
