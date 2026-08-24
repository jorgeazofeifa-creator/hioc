import importlib.util
import json
import pathlib
import types
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "tools" / "hioc-pe4-ha-auth-capability.py"
SPEC = importlib.util.spec_from_file_location("pe4_client", PATH)
CLIENT = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = CLIENT
SPEC.loader.exec_module(CLIENT)


ARGS = ["--expected-hostname", "a0d7b954-ssh", "--expected-operator", "root",
        "--target-ipv4", "192.168.100.251", "--target-port", "8123",
        "--instance-label", "PI5_HA"]


class FakeResponse:
    def __init__(self, status=200, body=b'{"message":"API running."}',
                 content_type="application/json", length=None):
        self.status, self.body, self.content_type, self.length = status, body, content_type, length
    def getheader(self, name, default=None):
        return {"Content-Type": self.content_type, "Content-Length": self.length}.get(name, default)
    def read(self, size=-1):
        return self.body[:size]


class FakeConnection:
    def __init__(self, response):
        self.response, self.requests, self.closed, self.sock = response, [], False, None
    def request(self, *args, **kwargs): self.requests.append((args, kwargs))
    def getresponse(self): return self.response
    def close(self): self.closed = True


class FakeWebSocket:
    def __init__(self, messages):
        self.messages = list(messages)
        self.sent = []
        self.timeouts = []
        self.closed = False
    def settimeout(self, value): self.timeouts.append(value)
    def recv(self): return self.messages.pop(0)
    def send(self, value): self.sent.append(value)
    def close(self): self.closed = True


class ClientTests(unittest.TestCase):
    def failure(self, callable_, code, stage):
        with self.assertRaises(CLIENT.ContractFailure) as caught: callable_()
        self.assertEqual((caught.exception.code, caught.exception.stage), (code, stage))

    def test_exact_cli(self):
        self.assertEqual(CLIENT.parse_args(ARGS).target_port, 8123)
        self.failure(lambda: CLIENT.parse_args(ARGS[:-2]), "INVALID_ARGUMENTS", "INPUT_VALIDATION")
        bad = ARGS.copy(); bad[-1] = "OTHER"
        self.failure(lambda: CLIENT.parse_args(bad), "INVALID_ARGUMENTS", "INPUT_VALIDATION")

    def test_dependency_preference_and_absence(self):
        self.assertEqual(CLIENT.detect_websocket_client(lambda n: object()), "PYTHON_WEBSOCKET_CLIENT")
        self.assertEqual(CLIENT.detect_websocket_client(lambda n: object() if n == "websockets" else None), "PYTHON_WEBSOCKETS")
        self.assertEqual(CLIENT.detect_websocket_client(lambda n: None), "ABSENT")

    def test_target_gates(self):
        args = CLIENT.parse_args(ARGS)
        good = dict(hostname="a0d7b954-ssh", operator="root", addresses={"192.168.100.251"},
                    stdin_tty=True, stderr_tty=True, shell="/bin/zsh")
        CLIENT.validate_target(args, **good)
        for field, value, code in (("hostname", "wrong", "WRONG_TARGET"),
                                   ("operator", "user", "WRONG_OPERATOR"),
                                   ("addresses", set(), "WRONG_TARGET"),
                                   ("shell", "/bin/fish", "UNSUPPORTED_SHELL")):
            changed = dict(good); changed[field] = value
            self.failure(lambda c=changed: CLIENT.validate_target(args, **c), code, "TARGET_IDENTITY")
        changed = dict(good); changed["stdin_tty"] = False
        self.failure(lambda: CLIENT.validate_target(args, **changed), "SECURE_PROMPT_UNAVAILABLE", "CREDENTIAL_ACQUISITION")

    def test_prompt(self):
        self.assertEqual(CLIENT.acquire_token(lambda _: "secret"), "secret")
        for result in ("", "bad\nvalue"):
            self.failure(lambda r=result: CLIENT.acquire_token(lambda _: r), "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
        self.failure(lambda: CLIENT.acquire_token(lambda _: (_ for _ in ()).throw(EOFError())),
                     "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")

    def check_rest_failure(self, response, code, stage):
        conn = FakeConnection(response)
        self.failure(lambda: CLIENT.rest_check("secret", lambda *a, **k: conn), code, stage)
        self.assertTrue(conn.closed)
        self.assertNotIn("secret", repr(response.body))

    def test_rest_pass_exact_request(self):
        conn = FakeConnection(FakeResponse())
        CLIENT.rest_check("secret", lambda *a, **k: conn)
        args, kwargs = conn.requests[0]
        self.assertEqual(args, ("GET", "/api/"))
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer secret")
        self.assertTrue(conn.closed)

    def test_rest_failures(self):
        cases = [(FakeResponse(status=401), "AUTHENTICATION_FAILED", "AUTHENTICATION"),
                 (FakeResponse(status=302), "UNAPPROVED_REDIRECT", "ENDPOINT"),
                 (FakeResponse(status=404), "UNEXPECTED_SCHEMA", "REST_CAPABILITY"),
                 (FakeResponse(status=500), "UNEXPECTED_SCHEMA", "REST_CAPABILITY"),
                 (FakeResponse(body=b"bad"), "UNEXPECTED_SCHEMA", "REST_CAPABILITY"),
                 (FakeResponse(body=b"{}"), "UNEXPECTED_SCHEMA", "REST_CAPABILITY"),
                 (FakeResponse(content_type="text/plain"), "UNEXPECTED_SCHEMA", "REST_CAPABILITY"),
                 (FakeResponse(body=b"x" * 65537), "RESPONSE_TOO_LARGE", "ENDPOINT")]
        for response, code, stage in cases:
            with self.subTest(code=code, status=response.status): self.check_rest_failure(response, code, stage)

    def test_rest_connection_failure(self):
        self.failure(lambda: CLIENT.rest_check("secret", lambda *a, **k: (_ for _ in ()).throw(OSError())),
                     "ENDPOINT_UNAVAILABLE", "ENDPOINT")

    def test_ws_message_schema(self):
        self.assertEqual(CLIENT._parse_ws_message('{"type":"auth_ok"}'), {"type": "auth_ok"})
        for raw, code in (("bad", "UNEXPECTED_SCHEMA"), ('{"type":"auth_ok","id":1}', "UNEXPECTED_SCHEMA"),
                          ("x" * 65537, "RESPONSE_TOO_LARGE")):
            self.failure(lambda r=raw: CLIENT._parse_ws_message(r), code, "WEBSOCKET_CAPABILITY")

    def test_websocket_client_auth_only_and_close(self):
        ws = FakeWebSocket(['{"type":"auth_required"}', '{"type":"auth_ok"}'])
        module = types.SimpleNamespace(create_connection=lambda *args, **kwargs: ws)
        with mock.patch.dict(sys.modules, {"websocket": module}):
            CLIENT.websocket_client_check("secret")
        self.assertTrue(ws.closed)
        self.assertEqual(len(ws.sent), 1)
        self.assertEqual(json.loads(ws.sent[0]), {"type": "auth", "access_token": "secret"})

    def test_websocket_client_auth_invalid(self):
        ws = FakeWebSocket(['{"type":"auth_required"}', '{"type":"auth_invalid"}'])
        module = types.SimpleNamespace(create_connection=lambda *args, **kwargs: ws)
        with mock.patch.dict(sys.modules, {"websocket": module}):
            self.failure(lambda: CLIENT.websocket_client_check("secret"),
                         "AUTHENTICATION_FAILED", "AUTHENTICATION")
        self.assertTrue(ws.closed)
        self.assertEqual(len(ws.sent), 1)

    def test_websocket_client_first_frame_and_connection_failures(self):
        ws = FakeWebSocket(['{"type":"auth_ok"}'])
        with mock.patch.dict(sys.modules, {"websocket": types.SimpleNamespace(
                create_connection=lambda *args, **kwargs: ws)}):
            self.failure(lambda: CLIENT.websocket_client_check("secret"),
                         "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
        with mock.patch.dict(sys.modules, {"websocket": types.SimpleNamespace(
                create_connection=lambda *args, **kwargs: (_ for _ in ()).throw(OSError()))}):
            self.failure(lambda: CLIENT.websocket_client_check("secret"),
                         "ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY")

    def test_output_contract_and_privacy(self):
        lines = CLIENT.success_lines("PYTHON_WEBSOCKET_CLIENT")
        CLIENT.validate_output(lines)
        self.assertEqual(lines[-6:], ["RESULT=PASS", "ERROR_CODE=NONE", "FAILURE_STAGE=COMPLETE",
                                      "ROLLBACK_RECOMMENDED=FALSE", "PE4_0B2A=COMPLETE", "PE4_0B2B=NOT_STARTED"])
        for unsafe in (["DETAIL=secret"], ["ERROR_CODE=TOKEN"], ["ERROR_CODE=BAD"],
                       ["RESULT={PASS}"], ["RESULT=192.168.1.1"]):
            self.failure(lambda u=unsafe: CLIENT.validate_output(u), "PRIVACY_CONTRACT_VIOLATION", "PRIVACY_VALIDATION")

    def test_failure_contract(self):
        for code in CLIENT.ERROR_CODES:
            for stage in ("ENDPOINT",):
                CLIENT.validate_output(CLIENT.failure_lines(code, stage))

    def test_proxy_detection_does_not_expose_values(self):
        self.assertTrue(CLIENT.proxy_influence_present({"HTTP_PROXY": "sensitive"}))
        self.assertFalse(CLIENT.proxy_influence_present({"HTTP_PROXY": ""}))

    @mock.patch.object(CLIENT, "websocket_client_check")
    @mock.patch.object(CLIENT, "rest_check")
    @mock.patch.object(CLIENT, "acquire_token", return_value="top-secret")
    @mock.patch.object(CLIENT, "validate_target")
    @mock.patch.object(CLIENT, "proxy_influence_present", return_value=False)
    @mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKET_CLIENT")
    @mock.patch.object(CLIENT, "parse_args")
    def test_run_sequence_and_no_secret_output(self, parse, dependency, proxy, target, prompt, rest, ws):
        parse.return_value = CLIENT.Arguments("a0d7b954-ssh", "root", "192.168.100.251", 8123, "PI5_HA")
        events = []
        prompt.side_effect = lambda: events.append("prompt") or "top-secret"
        rest.side_effect = lambda token, **kwargs: events.append("rest")
        ws.side_effect = lambda token, **kwargs: events.append("ws")
        output = []
        self.assertEqual(CLIENT.run(ARGS, output.append), 0)
        self.assertEqual(events, ["prompt", "rest", "ws"])
        self.assertNotIn("top-secret", "\n".join(output))
        self.assertNotIn("Authorization", "\n".join(output))

    @mock.patch.object(CLIENT, "detect_websocket_client", return_value="ABSENT")
    @mock.patch.object(CLIENT, "parse_args")
    def test_dependency_failure_before_prompt(self, parse, dependency):
        parse.return_value = CLIENT.Arguments("a0d7b954-ssh", "root", "192.168.100.251", 8123, "PI5_HA")
        with mock.patch.object(CLIENT, "acquire_token") as prompt:
            output = []
            self.assertEqual(CLIENT.run(ARGS, output.append), 1)
            prompt.assert_not_called()
        self.assertIn("ERROR_CODE=UNSUPPORTED_INTERFACE", output)

    @mock.patch.object(CLIENT, "websocket_client_check")
    @mock.patch.object(CLIENT, "rest_check", side_effect=CLIENT.ContractFailure("AUTHENTICATION_FAILED", "AUTHENTICATION"))
    @mock.patch.object(CLIENT, "acquire_token", return_value="secret")
    @mock.patch.object(CLIENT, "validate_target")
    @mock.patch.object(CLIENT, "proxy_influence_present", return_value=False)
    @mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKET_CLIENT")
    @mock.patch.object(CLIENT, "parse_args")
    def test_rest_failure_stops_websocket(self, parse, dependency, proxy, target, prompt, rest, ws):
        parse.return_value = CLIENT.Arguments("a0d7b954-ssh", "root", "192.168.100.251", 8123, "PI5_HA")
        self.assertEqual(CLIENT.run(ARGS, list().append), 1)
        ws.assert_not_called()

    def test_source_contains_no_forbidden_ha_commands_or_persistence(self):
        source = PATH.read_text(encoding="utf-8")
        for forbidden in ("/api/states", "subscribe_events", "config/device_registry/list",
                          ".storage/", "sqlite3", "mkdtemp", "NamedTemporaryFile"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
