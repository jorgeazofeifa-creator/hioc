#!/usr/bin/env python3
"""Validate PE-2 incident isolation without exposing operational incident data."""

import argparse
import ast
import json
import pathlib
import subprocess
import sys

CLASS_UNCHANGED = "INCIDENT_CONTRACT_UNCHANGED"
CLASS_DRIFT = "INCIDENT_OPERATIONAL_DRIFT"
CLASS_INCONCLUSIVE = "INCIDENT_VALIDATION_INCONCLUSIVE"
CLASS_REGRESSION = "INCIDENT_CONTRACT_REGRESSION"
ASSET_FIELDS = {"asset", "asset_id", "assets", "friendly_name", "physical_location", "purpose", "notes"}
REQUIRED = {
    "active": {"status", "severity", "system", "title"},
    "summary": {"correlation_engine"},
}


def _load(directory, name):
    path = pathlib.Path(directory) / name
    if not path.is_file():
        raise ValueError(f"missing_{name.removesuffix('.json')}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _walk(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def _contains_prohibited(documents, synthetic_values):
    folded = [value.casefold() for value in synthetic_values if value]
    for document in documents:
        for key, value in _walk(document):
            if key.casefold() in ASSET_FIELDS:
                return True
            if isinstance(value, str) and any(token in value.casefold() for token in folded):
                return True
    return False


def _schema_errors(active, history, summary):
    errors = []
    if not isinstance(active, dict) or not REQUIRED["active"].issubset(active): errors.append("active_schema")
    if not isinstance(history, list) or not all(isinstance(row, dict) for row in history): errors.append("history_schema")
    if not isinstance(summary, dict) or not REQUIRED["summary"].issubset(summary): errors.append("summary_schema")
    return errors


def _python_calls(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports, strings = set(), []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom): imports.add(node.module or "")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str): strings.append(node.value.casefold())
    return imports, strings


def prove_no_write_path(repo, implementation_commit):
    repo = pathlib.Path(repo)
    paths = [repo / "pi4/lib/hioc/assets.py", repo / "pi4/bin/hioc-assets.py", repo / "pi4/bin/hioc-validate-assets.py"]
    for path in paths:
        imports, strings = _python_calls(path)
        if any("incident" in name.casefold() or "mqtt" in name.casefold() for name in imports): return False
        if any("state/incidents" in value or "incidents/" in value or "incident-engine" in value for value in strings): return False
    changed = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", f"{implementation_commit}^", implementation_commit],
        check=True, capture_output=True, text=True,
    ).stdout.splitlines()
    prohibited = {"pi4/bin/hioc-incident-engine.sh", "pi4/bin/hioc-incident-engine-v2.py"}
    if prohibited & set(changed):
        return False
    installer_diff = subprocess.run(
        ["git", "-C", str(repo), "diff", "--unified=0", f"{implementation_commit}^", implementation_commit, "--", "pi4/install_pi4.sh"],
        check=True, capture_output=True, text=True,
    ).stdout.splitlines()
    changed_installer_lines = [line[1:].casefold() for line in installer_diff if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
    return not any("incident" in line or "cron_incident" in line for line in changed_installer_lines)


def compare(pre_dir, post_dir, repo, implementation_commit, synthetic_values=()):
    result = {
        "schema_version": 1, "classification": CLASS_INCONCLUSIVE,
        "active_schema_valid": False, "history_schema_valid": False, "summary_schema_valid": False,
        "asset_fields_present": False, "pe2_write_path_present": False,
        "protected_contract_regression": False, "operational_drift_detected": False,
        "causal_regression_demonstrated": False, "rollback_recommended": False, "warnings": [],
    }
    try:
        pre = [_load(pre_dir, name) for name in ("active.json", "history.json", "summary.json")]
        post = [_load(post_dir, name) for name in ("active.json", "history.json", "summary.json")]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result.update(warnings=[str(exc).split(":", 1)[0]])
        return result
    errors = _schema_errors(*pre) + _schema_errors(*post)
    result.update(active_schema_valid="active_schema" not in errors,
                  history_schema_valid="history_schema" not in errors,
                  summary_schema_valid="summary_schema" not in errors)
    prohibited_pre = _contains_prohibited(pre, synthetic_values)
    prohibited = _contains_prohibited(post, synthetic_values)
    write_path = not prove_no_write_path(repo, implementation_commit)
    result.update(asset_fields_present=prohibited, pe2_write_path_present=write_path)
    if (prohibited and not prohibited_pre) or write_path:
        result.update(classification=CLASS_REGRESSION, protected_contract_regression=True,
                      causal_regression_demonstrated=True, rollback_recommended=True,
                      warnings=sorted(set(errors)))
    elif errors or prohibited:
        result.update(classification=CLASS_INCONCLUSIVE, warnings=sorted(set(errors)))
    elif pre == post:
        result["classification"] = CLASS_UNCHANGED
    else:
        result.update(classification=CLASS_DRIFT, operational_drift_detected=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--pre", required=True); parser.add_argument("--post", required=True)
    parser.add_argument("--repo", required=True); parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--synthetic-value", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        result = compare(args.pre, args.post, args.repo, args.implementation_commit, args.synthetic_value)
    except Exception:
        result = {"schema_version": 1, "classification": CLASS_INCONCLUSIVE,
                  "causal_regression_demonstrated": False, "rollback_recommended": False,
                  "warnings": ["comparator_internal_error"]}
    print(json.dumps(result, indent=2, sort_keys=True))
    return {CLASS_UNCHANGED: 0, CLASS_DRIFT: 0, CLASS_INCONCLUSIVE: 40, CLASS_REGRESSION: 30}[result["classification"]]


if __name__ == "__main__": raise SystemExit(main())
