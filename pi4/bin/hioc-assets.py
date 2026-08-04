#!/usr/bin/env python3
"""Governed local-only PE-2.1 Asset CLI."""

import argparse
import json
import os
import sys
from pathlib import Path

HIOC_HOME = Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.assets import (AssetError, AssetPrivacyError, AssetService, AssetStore,
                         AssetUsageError, OPERATOR_FIELDS, error_envelope)


class AssetArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise AssetUsageError("INVALID_FIELD", "invalid CLI usage")


class AssetCli:
    def __init__(self, home: Path = HIOC_HOME, stdin=None, stdout=None, stderr=None):
        self.service = AssetService(AssetStore(home))
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    @staticmethod
    def parser():
        parser = AssetArgumentParser(description="Governed local HIOC Asset metadata")
        parser.add_argument("--json", action="store_true")
        sub = parser.add_subparsers(dest="command", required=True)
        sub.add_parser("initialize")
        sub.add_parser("list")
        show = sub.add_parser("show"); show.add_argument("--device-id", required=True); show.add_argument("--show-sensitive", action="store_true")
        setp = sub.add_parser("set"); setp.add_argument("--device-id", required=True)
        setp.add_argument("--friendly-name"); setp.add_argument("--physical-location"); setp.add_argument("--purpose"); setp.add_argument("--notes")
        setp.add_argument("--allow-orphan", action="store_true"); setp.add_argument("--expected-revision", type=int)
        clear = sub.add_parser("clear-field"); clear.add_argument("--device-id", required=True)
        clear.add_argument("--field", choices=OPERATOR_FIELDS, required=True); clear.add_argument("--expected-revision", type=int, required=True)
        remove = sub.add_parser("remove"); remove.add_argument("--device-id", required=True); remove.add_argument("--expected-revision", type=int, required=True)
        sub.add_parser("validate"); sub.add_parser("backup")
        restore = sub.add_parser("restore"); restore.add_argument("--backup", required=True)
        return parser

    def sensitive_allowed(self, args) -> bool:
        if not getattr(args, "show_sensitive", False):
            return False
        if args.json or not self.stdin.isatty() or not self.stdout.isatty():
            raise AssetPrivacyError("PRIVACY_REFUSED", "sensitive display requires a local interactive terminal")
        print("WARNING: sensitive local Asset values will be displayed. Type SHOW to continue:", file=self.stderr)
        if self.stdin.readline().strip() != "SHOW":
            raise AssetPrivacyError("PRIVACY_REFUSED", "sensitive display was cancelled")
        return True

    def execute(self, args):
        command = args.command
        if command == "initialize": return self.service.initialize()
        if command == "list": return self.service.list_assets()
        if command == "show": return self.service.show_asset(args.device_id, self.sensitive_allowed(args))
        if command == "set":
            fields = {}
            for option, field in (("friendly_name", "friendly_name"), ("physical_location", "physical_location"), ("purpose", "purpose"), ("notes", "notes")):
                value = getattr(args, option)
                if value is not None: fields[field] = value
            return self.service.set_fields(args.device_id, fields, args.allow_orphan, args.expected_revision)
        if command == "clear-field": return self.service.clear_field(args.device_id, args.field, args.expected_revision)
        if command == "remove": return self.service.remove(args.device_id, args.expected_revision)
        if command == "validate": return self.service.validate(refresh_status=True)
        if command == "backup": return self.service.backup()
        if command == "restore": return self.service.restore(args.backup)
        raise AssetUsageError("INVALID_FIELD", "invalid CLI usage")

    @staticmethod
    def human(result: dict) -> str:
        data = result["data"]
        fields = [f"RESULT={result['result'].upper()}", f"STATUS={result['status']}"]
        for key in ("asset_count", "device_id_digest", "revision", "changed_fields", "backup", "pre_restore_backup"):
            if key in data:
                value = data[key]
                if isinstance(value, list): value = ",".join(value)
                fields.append(f"{key.upper()}={value}")
        if "assets" in data:
            fields.append(f"RECORDS={len(data['assets'])}")
        if "values" in data:
            for key in OPERATOR_FIELDS:
                fields.append(f"{key.upper()}={data['values'][key]}")
        return " ".join(fields)

    def run(self, argv=None) -> int:
        command = "unknown"; json_mode = "--json" in (argv if argv is not None else sys.argv[1:])
        try:
            args = self.parser().parse_args(argv); command = args.command; json_mode = args.json
            result = self.execute(args)
        except AssetError as exc:
            result = error_envelope(command, exc)
            if json_mode: print(json.dumps(result, separators=(",", ":")), file=self.stdout)
            else: print(f"RESULT=ERROR ERROR_CODE={exc.code} MESSAGE={exc.safe_message}", file=self.stderr)
            return exc.exit_code
        except Exception:
            error = AssetError("INTERNAL_ERROR", "unexpected Asset command failure"); error.exit_code = 70
            result = error_envelope(command, error)
            if json_mode: print(json.dumps(result, separators=(",", ":")), file=self.stdout)
            else: print("RESULT=ERROR ERROR_CODE=INTERNAL_ERROR MESSAGE=unexpected Asset command failure", file=self.stderr)
            return 70
        if json_mode: print(json.dumps(result, ensure_ascii=False, separators=(",", ":")), file=self.stdout)
        else: print(self.human(result), file=self.stdout)
        return 0


def main(argv=None) -> int:
    return AssetCli().run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
