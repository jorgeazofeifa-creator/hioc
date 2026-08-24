#!/usr/bin/env python3
"""Governed PE-4.0B.2a Home Assistant authentication capability proof.

This tool is deliberately terminal-only. It persists no evidence and performs
exactly one REST request followed by one WebSocket authentication exchange.
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import http.client
import importlib
import importlib.util
import inspect
import json
import os
import re
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Callable, Sequence


EXPECTED_EXECUTION_HOSTNAME = "nutandpihole"
EXPECTED_EXECUTION_OPERATOR = "jazofv1"
EXPECTED_EXECUTION_IPV4 = "192.168.100.252"
HA_IPV4 = "192.168.100.251"
HA_PORT = 8123
INSTANCE_LABEL = "PI5_HA"
REST_PATH = "/api/"
WS_URI = "ws://192.168.100.251:8123/api/websocket"
CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 10.0
TOTAL_BUDGET = 20.0
MAX_MESSAGE = 65_536

ERROR_CODES = {
    "INVALID_ARGUMENTS", "WRONG_TARGET", "WRONG_OPERATOR", "UNSUPPORTED_SHELL",
    "SECURE_PROMPT_UNAVAILABLE", "AUTHENTICATION_UNAVAILABLE",
    "AUTHENTICATION_FAILED", "INSUFFICIENT_READ_SCOPE", "ENDPOINT_UNAVAILABLE",
    "UNAPPROVED_REDIRECT", "PROXY_INFLUENCE_DETECTED", "RESPONSE_TOO_LARGE",
    "REDIRECT_SUPPRESSION_UNAVAILABLE",
    "UNSUPPORTED_INTERFACE", "INTERFACE_CAPABILITY_MISSING", "UNEXPECTED_SCHEMA",
    "PRIVACY_CONTRACT_VIOLATION", "UNEXPECTED_ERROR",
}
STAGES = {
    "INPUT_VALIDATION", "TARGET_IDENTITY", "CREDENTIAL_ACQUISITION", "ENDPOINT",
    "AUTHENTICATION", "REST_CAPABILITY", "WEBSOCKET_CAPABILITY", "READ_SCOPE",
    "PRIVACY_VALIDATION", "WEBSOCKET_API_COMPATIBILITY", "COMPLETE",
}
ALLOWED_WS_CLASSES = {"PYTHON_WEBSOCKETS", "INCOMPATIBLE", "ABSENT"}
PROXY_NAMES = {
    "http_proxy", "https_proxy", "all_proxy", "no_proxy",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
}
ALLOWED_OUTPUT_VALUES = {
    "TARGET_IDENTITY": {"PASS"}, "ENDPOINT_POLICY": {"PASS"},
    "WEBSOCKET_CLIENT_CLASS": ALLOWED_WS_CLASSES, "CREDENTIAL_PROMPT": {"PASS"},
    "REDIRECT_SUPPRESSION_CAPABILITY": {"PASS"},
    "CREDENTIAL_ACQUIRED": {"TRUE"}, "REST_AUTHENTICATION": {"PASS"},
    "REST_CAPABILITY": {"SUPPORTED"}, "WEBSOCKET_AUTHENTICATION": {"PASS"},
    "WEBSOCKET_CAPABILITY": {"SUPPORTED"}, "READ_SCOPE": {"PASS"},
    "INSTANCE_REFERENCE_METHOD": {"OPERATOR_LOGICAL_LABEL"},
    "PRIVACY_VALIDATION": {"PASS"}, "RESULT": {"PASS", "FAIL"},
    "ERROR_CODE": ERROR_CODES | {"NONE"}, "FAILURE_STAGE": STAGES,
    "ROLLBACK_RECOMMENDED": {"FALSE"}, "PE4_0B2A": {"COMPLETE", "NOT_COMPLETE"},
    "PE4_0B2B": {"NOT_STARTED"},
}


class ContractFailure(Exception):
    def __init__(self, code: str, stage: str):
        self.code = code
        self.stage = stage
        super().__init__(code)


class ClosedArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ContractFailure("INVALID_ARGUMENTS", "INPUT_VALIDATION")


@dataclass(frozen=True)
class Arguments:
    expected_execution_hostname: str
    expected_execution_operator: str
    expected_execution_ipv4: str
    ha_ipv4: str
    ha_port: int
    instance_label: str


def parse_args(argv: Sequence[str]) -> Arguments:
    parser = ClosedArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--expected-execution-hostname", required=True)
    parser.add_argument("--expected-execution-operator", required=True)
    parser.add_argument("--expected-execution-ipv4", required=True)
    parser.add_argument("--ha-ipv4", required=True)
    parser.add_argument("--ha-port", required=True, type=int)
    parser.add_argument("--instance-label", required=True)
    ns = parser.parse_args(argv)
    args = Arguments(
        ns.expected_execution_hostname, ns.expected_execution_operator,
        ns.expected_execution_ipv4, ns.ha_ipv4, ns.ha_port, ns.instance_label,
    )
    if args != Arguments(
        EXPECTED_EXECUTION_HOSTNAME, EXPECTED_EXECUTION_OPERATOR,
        EXPECTED_EXECUTION_IPV4, HA_IPV4, HA_PORT, INSTANCE_LABEL,
    ):
        raise ContractFailure("INVALID_ARGUMENTS", "INPUT_VALIDATION")
    return args


def detect_websocket_client(
    find_spec: Callable[[str], object] = importlib.util.find_spec,
    import_module: Callable[[str], object] = importlib.import_module,
) -> str:
    if find_spec("websockets") is None:
        return "ABSENT"
    try:
        module = import_module("websockets")
        connect = getattr(module, "connect")
        parameters = inspect.signature(connect).parameters
    except (AttributeError, ImportError, TypeError, ValueError):
        return "INCOMPATIBLE"
    required = {"open_timeout", "close_timeout", "max_size", "proxy"}
    accepts_socket = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )
    redirect_handler = getattr(connect, "process_redirect", None)
    if (callable(connect) and required.issubset(parameters) and accepts_socket
            and callable(redirect_handler)):
        return "PYTHON_WEBSOCKETS"
    return "INCOMPATIBLE"


def proxy_influence_present(environ: dict[str, str]) -> bool:
    return any(environ.get(name, "").strip() for name in PROXY_NAMES)


def local_ipv4_addresses() -> set[str]:
    try:
        completed = subprocess.run(
            ["ip", "-o", "-4", "addr", "show"], capture_output=True, text=True,
            timeout=2, check=False, stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return set()
    if completed.returncode != 0:
        return set()
    return set(re.findall(r"\binet\s+(\d+\.\d+\.\d+\.\d+)/", completed.stdout))


def current_operator() -> str:
    try:
        import pwd
        return pwd.getpwuid(os.geteuid()).pw_name
    except (AttributeError, ImportError, KeyError, OSError):
        return ""


def validate_execution_host(args: Arguments, *, hostname: str, operator: str,
                            addresses: set[str], shell: str) -> None:
    if (hostname != args.expected_execution_hostname
            or args.expected_execution_ipv4 not in addresses):
        raise ContractFailure("WRONG_TARGET", "TARGET_IDENTITY")
    if operator != args.expected_execution_operator:
        raise ContractFailure("WRONG_OPERATOR", "TARGET_IDENTITY")
    shell_name = os.path.basename(shell).lower()
    if shell_name not in {"bash", "zsh", "ash"}:
        raise ContractFailure("UNSUPPORTED_SHELL", "TARGET_IDENTITY")


def validate_terminal(stdin_tty: bool, stderr_tty: bool) -> None:
    if not stdin_tty or not stderr_tty:
        raise ContractFailure("SECURE_PROMPT_UNAVAILABLE", "CREDENTIAL_ACQUISITION")


def acquire_token(prompt: Callable[[str], str] = getpass.getpass) -> str:
    try:
        token = prompt("Home Assistant access token: ")
    except (EOFError, KeyboardInterrupt, OSError, getpass.GetPassWarning):
        raise ContractFailure("AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION") from None
    if not token or "\r" in token or "\n" in token:
        raise ContractFailure("AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
    return token


def read_bounded(response: http.client.HTTPResponse) -> bytes:
    length = response.getheader("Content-Length")
    if length is not None:
        try:
            if int(length) > MAX_MESSAGE:
                raise ContractFailure("RESPONSE_TOO_LARGE", "ENDPOINT")
        except ValueError:
            raise ContractFailure("UNEXPECTED_SCHEMA", "REST_CAPABILITY") from None
    body = response.read(MAX_MESSAGE + 1)
    if len(body) > MAX_MESSAGE:
        raise ContractFailure("RESPONSE_TOO_LARGE", "ENDPOINT")
    return body


def remaining_timeout(deadline: float | None, cap: float, stage: str) -> float:
    if deadline is None:
        return cap
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ContractFailure("ENDPOINT_UNAVAILABLE", stage)
    return min(cap, remaining)


def rest_check(token: str, connection_factory: Callable[..., object] = http.client.HTTPConnection,
               deadline: float | None = None) -> None:
    connection = None
    try:
        connection = connection_factory(
            HA_IPV4, HA_PORT,
            timeout=remaining_timeout(deadline, CONNECT_TIMEOUT, "ENDPOINT"),
        )
        connection.request("GET", REST_PATH, headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Connection": "close",
        })
        if getattr(connection, "sock", None) is not None:
            connection.sock.settimeout(remaining_timeout(deadline, READ_TIMEOUT, "ENDPOINT"))
        response = connection.getresponse()
        if response.status == 401:
            raise ContractFailure("AUTHENTICATION_FAILED", "AUTHENTICATION")
        if 300 <= response.status < 400:
            raise ContractFailure("UNAPPROVED_REDIRECT", "ENDPOINT")
        if response.status != 200:
            raise ContractFailure("UNEXPECTED_SCHEMA", "REST_CAPABILITY")
        content_type = response.getheader("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type not in {"application/json", "application/vnd.api+json"} and not content_type.endswith("+json"):
            raise ContractFailure("UNEXPECTED_SCHEMA", "REST_CAPABILITY")
        try:
            value = json.loads(read_bounded(response).decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            raise ContractFailure("UNEXPECTED_SCHEMA", "REST_CAPABILITY") from None
        if value != {"message": "API running."}:
            raise ContractFailure("UNEXPECTED_SCHEMA", "REST_CAPABILITY")
    except ContractFailure:
        raise
    except (TimeoutError, OSError, http.client.HTTPException):
        raise ContractFailure("ENDPOINT_UNAVAILABLE", "ENDPOINT") from None
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass


def _parse_ws_message(raw: object) -> dict[str, object]:
    if not isinstance(raw, (str, bytes)):
        raise ContractFailure("UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
    if len(raw) > MAX_MESSAGE:
        raise ContractFailure("RESPONSE_TOO_LARGE", "WEBSOCKET_CAPABILITY")
    try:
        value = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError):
        raise ContractFailure("UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY") from None
    if not isinstance(value, dict) or set(value) != {"type"} or not isinstance(value["type"], str):
        raise ContractFailure("UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
    return value


def _dependency_rejected_oversized_message(exc: Exception, module: object) -> bool:
    exceptions = getattr(module, "exceptions", None)
    payload_too_big = getattr(exceptions, "PayloadTooBig", None)
    if isinstance(payload_too_big, type) and isinstance(exc, payload_too_big):
        return True
    for side in (getattr(exc, "rcvd", None), getattr(exc, "sent", None)):
        if getattr(side, "code", None) == 1009:
            return True
    return False


async def _websockets_async_check(
    token: str, deadline: float | None = None, websockets_module: object | None = None
) -> None:
    websockets = websockets_module or importlib.import_module("websockets")
    connect = websockets.connect
    parameters = inspect.signature(connect).parameters
    required = {"open_timeout", "close_timeout", "max_size", "proxy"}
    if not required.issubset(parameters) or not any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    ) or not callable(getattr(connect, "process_redirect", None)):
        raise ContractFailure(
            "REDIRECT_SUPPRESSION_UNAVAILABLE", "WEBSOCKET_API_COMPATIBILITY"
        )
    connected_socket = None
    try:
        connected_socket = socket.create_connection(
            (HA_IPV4, HA_PORT),
            timeout=remaining_timeout(deadline, CONNECT_TIMEOUT, "WEBSOCKET_CAPABILITY"),
        )
        async with connect(
            WS_URI,
            open_timeout=remaining_timeout(deadline, CONNECT_TIMEOUT, "WEBSOCKET_CAPABILITY"),
            close_timeout=remaining_timeout(deadline, CONNECT_TIMEOUT, "WEBSOCKET_CAPABILITY"),
            max_size=MAX_MESSAGE, proxy=None, sock=connected_socket,
        ) as ws:
            first = await asyncio.wait_for(
                ws.recv(), remaining_timeout(deadline, READ_TIMEOUT, "WEBSOCKET_CAPABILITY")
            )
            if _parse_ws_message(first)["type"] != "auth_required":
                raise ContractFailure("UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
            await ws.send(json.dumps({"type": "auth", "access_token": token}, separators=(",", ":")))
            kind = _parse_ws_message(await asyncio.wait_for(
                ws.recv(), remaining_timeout(deadline, READ_TIMEOUT, "WEBSOCKET_CAPABILITY")
            ))["type"]
            if kind == "auth_invalid":
                raise ContractFailure("AUTHENTICATION_FAILED", "AUTHENTICATION")
            if kind != "auth_ok":
                raise ContractFailure("UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
    except ContractFailure:
        raise
    except (TimeoutError, OSError, asyncio.TimeoutError):
        raise ContractFailure("ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY") from None
    except Exception as exc:
        if _dependency_rejected_oversized_message(exc, websockets):
            raise ContractFailure("RESPONSE_TOO_LARGE", "WEBSOCKET_CAPABILITY") from None
        current: BaseException | None = exc
        while current is not None:
            response = getattr(current, "response", None)
            status = getattr(response, "status_code", getattr(response, "status", None))
            if isinstance(status, int) and 300 <= status < 400:
                raise ContractFailure("UNAPPROVED_REDIRECT", "ENDPOINT") from None
            current = current.__cause__
        raise ContractFailure("INTERFACE_CAPABILITY_MISSING", "WEBSOCKET_CAPABILITY") from None
    finally:
        if connected_socket is not None:
            try:
                connected_socket.close()
            except OSError:
                pass


def websockets_check(
    token: str, deadline: float | None = None, websockets_module: object | None = None
) -> None:
    asyncio.run(_websockets_async_check(token, deadline, websockets_module))


def success_lines(ws_class: str) -> list[str]:
    return [
        "TARGET_IDENTITY=PASS", "ENDPOINT_POLICY=PASS",
        f"WEBSOCKET_CLIENT_CLASS={ws_class}",
        "REDIRECT_SUPPRESSION_CAPABILITY=PASS", "CREDENTIAL_PROMPT=PASS",
        "CREDENTIAL_ACQUIRED=TRUE", "REST_AUTHENTICATION=PASS",
        "REST_CAPABILITY=SUPPORTED", "WEBSOCKET_AUTHENTICATION=PASS",
        "WEBSOCKET_CAPABILITY=SUPPORTED", "READ_SCOPE=PASS",
        "INSTANCE_REFERENCE_METHOD=OPERATOR_LOGICAL_LABEL", "PRIVACY_VALIDATION=PASS",
        "RESULT=PASS", "ERROR_CODE=NONE", "FAILURE_STAGE=COMPLETE",
        "ROLLBACK_RECOMMENDED=FALSE", "PE4_0B2A=COMPLETE", "PE4_0B2B=NOT_STARTED",
    ]


def failure_lines(code: str, stage: str, ws_class: str | None = None) -> list[str]:
    lines = []
    if ws_class in ALLOWED_WS_CLASSES:
        lines.append(f"WEBSOCKET_CLIENT_CLASS={ws_class}")
    lines.extend(["RESULT=FAIL", f"ERROR_CODE={code}", f"FAILURE_STAGE={stage}",
                  "ROLLBACK_RECOMMENDED=FALSE", "PE4_0B2A=NOT_COMPLETE",
                  "PE4_0B2B=NOT_STARTED"])
    return lines


def validate_output(lines: Sequence[str]) -> None:
    forbidden = re.compile(
        r"(?i)(authorization|bearer|token|wss?://|https?://|(?:[0-9a-f]{2}:){5}[0-9a-f]{2}|"
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b[a-z0-9_]+\.[a-z0-9_]+\b|[{}\[\]])"
    )
    for line in lines:
        if len(line) > 128 or "\r" in line or "\n" in line or "=" not in line:
            raise ContractFailure("PRIVACY_CONTRACT_VIOLATION", "PRIVACY_VALIDATION")
        key, value = line.split("=", 1)
        if key not in ALLOWED_OUTPUT_VALUES or value not in ALLOWED_OUTPUT_VALUES[key]:
            raise ContractFailure("PRIVACY_CONTRACT_VIOLATION", "PRIVACY_VALIDATION")
        if forbidden.search(line):
            raise ContractFailure("PRIVACY_CONTRACT_VIOLATION", "PRIVACY_VALIDATION")


def emit(lines: Sequence[str], output: Callable[[str], None] = print) -> None:
    validate_output(lines)
    for line in lines:
        output(line)


def run(argv: Sequence[str], output: Callable[[str], None] = print) -> int:
    ws_class: str | None = None
    token: str | None = None
    started = time.monotonic()
    deadline = started + TOTAL_BUDGET
    try:
        args = parse_args(argv)
        validate_execution_host(
            args, hostname=socket.gethostname(), operator=current_operator(),
            addresses=local_ipv4_addresses(), shell=os.environ.get("SHELL", ""),
        )
        if proxy_influence_present(dict(os.environ)):
            raise ContractFailure("PROXY_INFLUENCE_DETECTED", "ENDPOINT")
        ws_class = detect_websocket_client()
        if ws_class == "ABSENT":
            raise ContractFailure("UNSUPPORTED_INTERFACE", "WEBSOCKET_CAPABILITY")
        if ws_class == "INCOMPATIBLE":
            raise ContractFailure(
                "REDIRECT_SUPPRESSION_UNAVAILABLE", "WEBSOCKET_API_COMPATIBILITY"
            )
        validate_terminal(sys.stdin.isatty(), sys.stderr.isatty())
        token = acquire_token()
        rest_check(token, deadline=deadline)
        if time.monotonic() - started >= TOTAL_BUDGET:
            raise ContractFailure("ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY")
        websockets_check(token, deadline=deadline)
        if time.monotonic() - started > TOTAL_BUDGET:
            raise ContractFailure("ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY")
        emit(success_lines(ws_class), output)
        return 0
    except ContractFailure as exc:
        try:
            emit(failure_lines(exc.code, exc.stage, ws_class), output)
        except ContractFailure:
            for line in failure_lines("PRIVACY_CONTRACT_VIOLATION", "PRIVACY_VALIDATION"):
                output(line)
        return 1
    except SystemExit:
        raise
    except Exception:
        emit(failure_lines("UNEXPECTED_ERROR", "INPUT_VALIDATION", ws_class), output)
        return 1
    finally:
        token = None


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
