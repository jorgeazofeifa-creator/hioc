import importlib.util
import asyncio
import json
import io
import warnings
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


ARGS = ["--expected-execution-hostname", "nutandpihole",
        "--expected-execution-operator", "jazofv1",
        "--expected-execution-ipv4", "192.168.100.252",
        "--ha-ipv4", "192.168.100.251", "--ha-port", "8123",
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
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, traceback): self.closed = True
    async def recv(self):
        value = self.messages.pop(0)
        if isinstance(value, Exception): raise value
        return value
    async def send(self, value): self.sent.append(value)


class FakePayloadTooBig(Exception):
    pass


def compatible_connect(*args, open_timeout=None, close_timeout=None, max_size=None,
                       proxy=None, **kwargs):
    raise AssertionError("not called during dependency detection")


def reject_redirect(self, exc):
    return exc


compatible_connect.process_redirect = reject_redirect


class ClientTests(unittest.TestCase):
    def failure(self, callable_, code, stage):
        with self.assertRaises(CLIENT.ContractFailure) as caught: callable_()
        self.assertEqual((caught.exception.code, caught.exception.stage), (code, stage))

    def test_exact_cli(self):
        self.assertEqual(CLIENT.parse_args(ARGS).ha_port, 8123)
        self.failure(lambda: CLIENT.parse_args(ARGS[:-2]), "INVALID_ARGUMENTS", "INPUT_VALIDATION")
        bad = ARGS.copy(); bad[-1] = "OTHER"
        self.failure(lambda: CLIENT.parse_args(bad), "INVALID_ARGUMENTS", "INPUT_VALIDATION")

    def test_dependency_preference_and_absence(self):
        module = types.SimpleNamespace(connect=compatible_connect)
        self.assertEqual(CLIENT.detect_websocket_client(lambda n: object(), lambda n: module), "PYTHON_WEBSOCKETS")
        self.assertEqual(CLIENT.detect_websocket_client(lambda n: None), "ABSENT")
        incompatible = types.SimpleNamespace(connect=lambda uri: None)
        self.assertEqual(CLIENT.detect_websocket_client(
            lambda n: object(), lambda n: incompatible), "INCOMPATIBLE")

    def test_execution_host_gates_are_separate_from_ha_endpoint(self):
        args = CLIENT.parse_args(ARGS)
        good = dict(hostname="nutandpihole", operator="jazofv1", addresses={"192.168.100.252"},
                    shell="/bin/zsh")
        CLIENT.validate_execution_host(args, **good)
        self.assertNotIn(CLIENT.HA_IPV4, good["addresses"])
        for field, value, code in (("hostname", "wrong", "WRONG_TARGET"),
                                   ("operator", "user", "WRONG_OPERATOR"),
                                   ("addresses", set(), "WRONG_TARGET"),
                                   ("shell", "/bin/fish", "UNSUPPORTED_SHELL")):
            changed = dict(good); changed[field] = value
            self.failure(lambda c=changed: CLIENT.validate_execution_host(args, **c), code, "TARGET_IDENTITY")
        CLIENT.validate_terminal(True, True)
        self.failure(lambda: CLIENT.validate_terminal(False, True),
                     "SECURE_PROMPT_UNAVAILABLE", "CREDENTIAL_ACQUISITION")

    def test_prompt(self):
        self.assertEqual(CLIENT.acquire_token(lambda _: "secret"), "secret")
        for result in ("", "bad\nvalue", "bad\rvalue"):
            self.failure(lambda r=result: CLIENT.acquire_token(lambda _: r), "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
        for error in (EOFError, KeyboardInterrupt, OSError):
            with self.subTest(error=error.__name__):
                self.failure(lambda e=error: CLIENT.acquire_token(
                    lambda _: (_ for _ in ()).throw(e())),
                    "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")

    def test_getpass_warning_fails_before_prompt_continuation(self):
        continued = mock.Mock(return_value="must-not-return")
        def prompt(label):
            warnings.warn("PRIVATE_WARNING_SENTINEL", CLIENT.getpass.GetPassWarning)
            return continued()
        self.failure(lambda: CLIENT.acquire_token(prompt),
                     "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
        continued.assert_not_called()

    def test_real_getpass_fallback_never_reads_input_or_prints_diagnostic(self):
        stream = io.StringIO()
        with mock.patch.object(CLIENT.getpass, "_raw_input") as raw_input:
            self.failure(lambda: CLIENT.acquire_token(
                lambda label: CLIENT.getpass.fallback_getpass(label, stream=stream)),
                "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
        raw_input.assert_not_called()
        self.assertEqual(stream.getvalue(), "")

    def test_prompt_warning_filter_restored_on_success_and_failure(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", CLIENT.getpass.GetPassWarning)
            original_filters = warnings.filters[:]
            self.assertEqual(CLIENT.acquire_token(lambda _: "synthetic-secret"), "synthetic-secret")
            self.assertEqual(warnings.filters, original_filters)
            self.failure(lambda: CLIENT.acquire_token(lambda _: warnings.warn(
                "PRIVATE_WARNING_SENTINEL", CLIENT.getpass.GetPassWarning)),
                "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
            self.assertEqual(warnings.filters, original_filters)
            warnings.warn("outside-context", CLIENT.getpass.GetPassWarning)
            self.assertEqual(len(caught), 1)
            self.assertEqual(str(caught[0].message), "outside-context")

    def test_run_getpass_warning_stops_before_clock_and_network(self):
        original_acquire = CLIENT.acquire_token
        stream = io.StringIO()
        output = []
        with mock.patch.object(CLIENT, "validate_execution_host"), \
             mock.patch.object(CLIENT, "local_ipv4_addresses", return_value=set()), \
             mock.patch.object(CLIENT, "current_operator", return_value="fixture"), \
             mock.patch.object(CLIENT, "proxy_influence_present", return_value=False), \
             mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKETS"), \
             mock.patch.object(CLIENT, "validate_terminal"), \
             mock.patch.object(CLIENT.getpass, "_raw_input") as raw_input, \
             mock.patch.object(CLIENT, "acquire_token", side_effect=lambda: original_acquire(
                 lambda label: CLIENT.getpass.fallback_getpass(label, stream=stream))), \
             mock.patch.object(CLIENT.time, "monotonic") as clock, \
             mock.patch.object(CLIENT, "rest_check") as rest, \
             mock.patch.object(CLIENT, "websockets_check") as ws, \
             mock.patch.object(CLIENT.socket, "create_connection") as connection:
            self.assertEqual(CLIENT.run(ARGS, output.append), 1)
        for operation in (raw_input, clock, rest, ws, connection):
            operation.assert_not_called()
        self.assertEqual(stream.getvalue(), "")
        self.assertEqual(output, CLIENT.failure_lines(
            "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION", "PYTHON_WEBSOCKETS"))
        for forbidden in ("Warning:", "GetPassWarning", "echoed", "Traceback"):
            self.assertNotIn(forbidden, "\n".join(output))

    def check_rest_failure(self, response, code, stage):
        conn = FakeConnection(response)
        self.failure(lambda: CLIENT.rest_check("secret", lambda *a, **k: conn), code, stage)
        self.assertTrue(conn.closed)
        self.assertNotIn("secret", repr(response.body))

    def test_rest_pass_exact_request(self):
        conn = FakeConnection(FakeResponse())
        endpoint = []
        def factory(*args, **kwargs):
            endpoint.append((args, kwargs))
            return conn
        CLIENT.rest_check("secret", factory)
        self.assertEqual(endpoint[0][0], ("192.168.100.251", 8123))
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
        frame = {"type": "auth_ok", "ha_version": "2026.8.1"}
        self.assertEqual(CLIENT._parse_ws_message(json.dumps(frame)), frame)
        for raw in ("bad", "[]", "null", "1", '"text"', "{}",
                    '{"type":null}', '{"type":1}', b"\xff", object()):
            with self.subTest(raw=raw):
                self.failure(lambda: CLIENT._parse_ws_message(raw),
                             "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
        self.failure(lambda: CLIENT._parse_ws_message("x" * 65537),
                     "RESPONSE_TOO_LARGE", "WEBSOCKET_CAPABILITY")

    def test_documented_auth_schemas_discard_ancillary_fields(self):
        self.assertIsNone(CLIENT._parse_auth_required(
            b'{"type":"auth_required","ha_version":"2026.8.1"}'))
        self.assertIsNone(CLIENT._parse_auth_result(
            '{"type":"auth_ok","ha_version":"2026.8.1"}'))
        self.failure(lambda: CLIENT._parse_auth_result(
            '{"type":"auth_invalid","message":"Invalid access token or password"}'),
            "AUTHENTICATION_FAILED", "AUTHENTICATION")

    def test_exact_phase_schemas_reject_missing_wrong_and_extra_fields(self):
        for kind, field, parser in (
                ("auth_required", "ha_version", CLIENT._parse_auth_required),
                ("auth_ok", "ha_version", CLIENT._parse_auth_result),
                ("auth_invalid", "message", CLIENT._parse_auth_result)):
            cases = [{"type": kind}, {"type": kind, field: "text", "id": 1}]
            cases.extend({"type": kind, field: value}
                         for value in (1, None, {}, [], True))
            for frame in cases:
                with self.subTest(frame=frame):
                    self.failure(lambda: parser(json.dumps(frame)),
                                 "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")

    def test_wrong_phase_and_command_frames_rejected(self):
        for parser, wrong_auth in (
                (CLIENT._parse_auth_required, {"type": "auth_ok", "ha_version": "2026.8.1"}),
                (CLIENT._parse_auth_result, {"type": "auth_required", "ha_version": "2026.8.1"})):
            wrong_frames = [wrong_auth]
            if parser is CLIENT._parse_auth_required:
                wrong_frames.append({"type": "auth_invalid", "message": "bad"})
            for frame in wrong_frames:
                self.failure(lambda: parser(json.dumps(frame)),
                             "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
            for kind in ("result", "event", "pong", "supported_features", "arbitrary"):
                with self.subTest(parser=parser.__name__, kind=kind):
                    self.failure(lambda: parser(json.dumps({"type": kind})),
                                 "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")

    def test_real_exchange_terminal_privacy_success_and_failure(self):
        version = "PRIVATE_VERSION_SENTINEL"
        message = "PRIVATE_SERVER_MESSAGE_SENTINEL"
        for result, expected_code in (
                ({"type": "auth_ok", "ha_version": version}, None),
                ({"type": "auth_invalid", "message": message}, "AUTHENTICATION_FAILED")):
            with self.subTest(result=result["type"]):
                ws = FakeWebSocket([json.dumps({"type": "auth_required", "ha_version": version}),
                                    json.dumps(result)])
                def connect(uri, *, open_timeout=None, close_timeout=None,
                            max_size=None, proxy=None, **kwargs):
                    return ws
                connect.process_redirect = reject_redirect
                module = types.SimpleNamespace(connect=connect)
                output = []
                sock = mock.Mock()
                with mock.patch.object(CLIENT, "validate_execution_host"), \
                     mock.patch.object(CLIENT, "local_ipv4_addresses", return_value=set()), \
                     mock.patch.object(CLIENT, "current_operator", return_value="fixture"), \
                     mock.patch.object(CLIENT, "proxy_influence_present", return_value=False), \
                     mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKETS"), \
                     mock.patch.object(CLIENT, "validate_terminal"), \
                     mock.patch.object(CLIENT, "acquire_token", return_value="fixture-secret"), \
                     mock.patch.object(CLIENT, "rest_check"), \
                     mock.patch.object(CLIENT.importlib, "import_module", return_value=module), \
                     mock.patch.object(CLIENT.socket, "create_connection", return_value=sock):
                    self.assertEqual(CLIENT.run(ARGS, output.append), int(expected_code is not None))
                expected = (CLIENT.success_lines("PYTHON_WEBSOCKETS") if expected_code is None
                            else CLIENT.failure_lines(expected_code, "AUTHENTICATION", "PYTHON_WEBSOCKETS"))
                self.assertEqual(output, expected)
                self.assertIn("PE4_0B2B=NOT_STARTED", output)
                for private in (version, message, "fixture-secret", "Authorization", CLIENT.HA_IPV4, CLIENT.WS_URI):
                    self.assertNotIn(private, "\n".join(output))
                self.assertEqual([json.loads(raw) for raw in ws.sent],
                                 [{"type": "auth", "access_token": "fixture-secret"}])
                self.assertEqual(ws.messages, [])
                self.assertTrue(ws.closed)
                sock.close.assert_called_once_with()

    def test_websockets_auth_only_receive_bound_and_close(self):
        ws = FakeWebSocket(['{"type":"auth_required","ha_version":"2026.8.1"}', '{"type":"auth_ok","ha_version":"2026.8.1"}'])
        captured = {}
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None, proxy=None,
                    **kwargs):
            captured.update(uri=uri, open_timeout=open_timeout, close_timeout=close_timeout,
                            max_size=max_size, proxy=proxy, sock=kwargs.get("sock"))
            return ws
        connect.process_redirect = reject_redirect
        module = types.SimpleNamespace(connect=connect, exceptions=types.SimpleNamespace(
            PayloadTooBig=FakePayloadTooBig))
        fake_socket = mock.Mock()
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=fake_socket) as create:
            asyncio.run(CLIENT._websockets_async_check("secret", websockets_module=module))
        create.assert_called_once_with(("192.168.100.251", 8123), timeout=5.0)
        self.assertTrue(ws.closed)
        self.assertEqual(len(ws.sent), 1)
        self.assertEqual(json.loads(ws.sent[0]), {"type": "auth", "access_token": "secret"})
        self.assertEqual(captured["max_size"], 65_536)
        self.assertIsNone(captured["proxy"])
        self.assertIs(captured["sock"], fake_socket)

    def test_stalled_auth_send_closes_reaps_and_never_receives_again(self):
        async def exercise(unblock_on_close):
            close_event = asyncio.Event()
            tasks = []
            events = []
            class StalledWebSocket(FakeWebSocket):
                async def send(self, value):
                    self.sent.append(value)
                    tasks.append(asyncio.current_task())
                    events.append("send")
                    try:
                        await close_event.wait()
                    finally:
                        events.append("send_finished")
                async def close(self):
                    events.append("close")
                    if unblock_on_close:
                        close_event.set()
            ws = StalledWebSocket(['{"type":"auth_required","ha_version":"synthetic"}',
                                   '{"type":"auth_ok","ha_version":"synthetic"}'])
            def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None,
                        proxy=None, **kwargs):
                return ws
            connect.process_redirect = reject_redirect
            sock = mock.Mock()
            with mock.patch.object(CLIENT.socket, "create_connection", return_value=sock):
                with self.assertRaises(CLIENT.ContractFailure) as caught:
                    await CLIENT._websockets_async_check(
                        "synthetic-secret", deadline=CLIENT.time.monotonic() + 0.02,
                        websockets_module=types.SimpleNamespace(connect=connect))
            self.assertEqual((caught.exception.code, caught.exception.stage),
                             ("ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY"))
            self.assertEqual(len(ws.sent), 1)
            self.assertEqual(json.loads(ws.sent[0]), {"type": "auth", "access_token": "synthetic-secret"})
            self.assertEqual(len(ws.messages), 1)
            self.assertTrue(ws.closed)
            self.assertLess(events.index("close"), events.index("send_finished"))
            self.assertTrue(all(task.done() for task in tasks))
            self.assertEqual(asyncio.all_tasks(), {asyncio.current_task()})
            sock.close.assert_called_once_with()
            output = CLIENT.failure_lines(caught.exception.code, caught.exception.stage)
            CLIENT.validate_output(output)
            for private in ("synthetic-secret", "access_token", "Bearer", "Authorization", "Traceback"):
                self.assertNotIn(private, "\n".join(output))
        for unblock_on_close in (True, False):
            with self.subTest(unblock_on_close=unblock_on_close):
                asyncio.run(exercise(unblock_on_close))

    def test_stalled_close_aborts_transport_and_reaps_send(self):
        async def exercise():
            never = asyncio.Event()
            tasks = []
            class StalledClose:
                transport = mock.Mock()
                async def send(self, value):
                    tasks.append(asyncio.current_task())
                    await never.wait()
                async def close(self):
                    await never.wait()
            ws = StalledClose()
            with mock.patch.object(CLIENT, "CONNECT_TIMEOUT", 0.01):
                with self.assertRaises(CLIENT.ContractFailure) as caught:
                    await CLIENT._send_auth(ws, "synthetic-secret", CLIENT.time.monotonic() + 0.01)
            self.assertEqual(caught.exception.code, "ENDPOINT_UNAVAILABLE")
            ws.transport.abort.assert_called_once_with()
            self.assertTrue(all(task.done() for task in tasks))
            self.assertEqual(asyncio.all_tasks(), {asyncio.current_task()})
        asyncio.run(exercise())

    def test_run_stalled_send_failure_output_is_private(self):
        class StalledWebSocket(FakeWebSocket):
            async def send(self, value):
                self.sent.append(value)
                await asyncio.Event().wait()
            async def close(self):
                self.closed = True
        ws = StalledWebSocket(['{"type":"auth_required","ha_version":"private-version"}'])
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None,
                    proxy=None, **kwargs):
            return ws
        connect.process_redirect = reject_redirect
        output = []
        sock = mock.Mock()
        with mock.patch.object(CLIENT, "validate_execution_host"), \
             mock.patch.object(CLIENT, "local_ipv4_addresses", return_value=set()), \
             mock.patch.object(CLIENT, "current_operator", return_value="fixture"), \
             mock.patch.object(CLIENT, "proxy_influence_present", return_value=False), \
             mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKETS"), \
             mock.patch.object(CLIENT, "validate_terminal"), \
             mock.patch.object(CLIENT, "acquire_token", return_value="synthetic-secret"), \
             mock.patch.object(CLIENT, "rest_check"), \
             mock.patch.object(CLIENT, "TOTAL_BUDGET", 0.02), \
             mock.patch.object(CLIENT.importlib, "import_module", return_value=types.SimpleNamespace(connect=connect)), \
             mock.patch.object(CLIENT.socket, "create_connection", return_value=sock):
            self.assertEqual(CLIENT.run(ARGS, output.append), 1)
        self.assertEqual(output, CLIENT.failure_lines(
            "ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY", "PYTHON_WEBSOCKETS"))
        self.assertEqual(len(ws.sent), 1)
        self.assertTrue(ws.closed)
        sock.close.assert_called_once_with()
        for private in ("synthetic-secret", "private-version", "access_token", "Bearer", "Traceback"):
            self.assertNotIn(private, "\n".join(output))

    def test_auth_send_uses_remaining_shared_deadline(self):
        async def exercise():
            ws = FakeWebSocket([])
            original_wait = asyncio.wait
            captured = []
            async def wait(tasks, *, timeout):
                captured.append(timeout)
                return await original_wait(tasks, timeout=timeout)
            with mock.patch.object(CLIENT.time, "monotonic", return_value=7.0), \
                 mock.patch.object(CLIENT.asyncio, "wait", side_effect=wait):
                await CLIENT._send_auth(ws, "synthetic-secret", 20.0)
            self.assertEqual(captured, [13.0])
            self.assertEqual(len(ws.sent), 1)
        asyncio.run(exercise())

    def test_expired_auth_send_deadline_creates_no_send_work(self):
        ws = mock.Mock()
        with mock.patch.object(CLIENT.time, "monotonic", return_value=20.0):
            self.failure(lambda: asyncio.run(CLIENT._send_auth(ws, "synthetic-secret", 20.0)),
                         "ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY")
        ws.send.assert_not_called()

    def test_auth_send_exception_maps_without_secret_output(self):
        class FailedSend(FakeWebSocket):
            async def send(self, value):
                raise OSError("synthetic-secret")
        ws = FailedSend(['{"type":"auth_required","ha_version":"synthetic"}'])
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None,
                    proxy=None, **kwargs):
            return ws
        connect.process_redirect = reject_redirect
        sock = mock.Mock()
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=sock):
            self.failure(lambda: asyncio.run(CLIENT._websockets_async_check(
                "synthetic-secret", websockets_module=types.SimpleNamespace(connect=connect))),
                "ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY")
        self.assertTrue(ws.closed)
        sock.close.assert_called_once_with()

    def test_websockets_auth_invalid(self):
        ws = FakeWebSocket(['{"type":"auth_required","ha_version":"2026.8.1"}', '{"type":"auth_invalid","message":"Invalid access token or password"}'])
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None, proxy=None,
                    **kwargs):
            return ws
        connect.process_redirect = reject_redirect
        module = types.SimpleNamespace(
            connect=connect,
            exceptions=types.SimpleNamespace(PayloadTooBig=FakePayloadTooBig))
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=mock.Mock()):
            self.failure(lambda: asyncio.run(CLIENT._websockets_async_check(
                "secret", websockets_module=module)), "AUTHENTICATION_FAILED", "AUTHENTICATION")
        self.assertTrue(ws.closed)
        self.assertEqual(len(ws.sent), 1)

    def test_websockets_first_frame_and_connection_failures(self):
        ws = FakeWebSocket(['{"type":"auth_ok","ha_version":"2026.8.1"}'])
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None, proxy=None,
                    **kwargs):
            return ws
        connect.process_redirect = reject_redirect
        module = types.SimpleNamespace(connect=connect,
                                       exceptions=types.SimpleNamespace(PayloadTooBig=FakePayloadTooBig))
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=mock.Mock()):
            self.failure(lambda: asyncio.run(CLIENT._websockets_async_check(
                "secret", websockets_module=module)), "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
        def failing_connect(uri, *, open_timeout=None, close_timeout=None, max_size=None, proxy=None,
                            **kwargs):
            raise OSError()
        failing_connect.process_redirect = reject_redirect
        module = types.SimpleNamespace(
            connect=failing_connect,
            exceptions=types.SimpleNamespace(PayloadTooBig=FakePayloadTooBig))
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=mock.Mock()):
            self.failure(lambda: asyncio.run(CLIENT._websockets_async_check(
                "secret", websockets_module=module)), "ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY")

    def test_dependency_level_oversize_maps_before_materialized_message(self):
        ws = FakeWebSocket([FakePayloadTooBig("oversized")])
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None, proxy=None,
                    **kwargs):
            return ws
        connect.process_redirect = reject_redirect
        module = types.SimpleNamespace(connect=connect,
                                       exceptions=types.SimpleNamespace(PayloadTooBig=FakePayloadTooBig))
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=mock.Mock()):
            self.failure(lambda: asyncio.run(CLIENT._websockets_async_check(
                "secret", websockets_module=module)), "RESPONSE_TOO_LARGE", "WEBSOCKET_CAPABILITY")

    def test_redirect_is_rejected_by_actual_socket_bound_connection_path(self):
        class RedirectResponse:
            status_code = 302

        class RedirectStatus(Exception):
            response = RedirectResponse()

        class RedirectRefused(ValueError):
            pass

        calls = []
        def connect(uri, *, open_timeout=None, close_timeout=None, max_size=None,
                    proxy=None, **kwargs):
            calls.append((uri, kwargs.get("sock")))
            refused = RedirectRefused("redirect refused for pre-existing socket")
            refused.__cause__ = RedirectStatus()
            raise refused
        connect.process_redirect = reject_redirect
        module = types.SimpleNamespace(
            connect=connect,
            exceptions=types.SimpleNamespace(PayloadTooBig=FakePayloadTooBig),
        )
        fake_socket = mock.Mock()
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=fake_socket):
            self.failure(lambda: asyncio.run(CLIENT._websockets_async_check(
                "never-send-this-token", websockets_module=module)),
                "UNAPPROVED_REDIRECT", "ENDPOINT")
        self.assertEqual(calls, [(CLIENT.WS_URI, fake_socket)])
        self.assertNotIn("never-send-this-token", repr(calls))

    def test_redirect_capability_missing_fails_before_prompt(self):
        def incompatible_connect(uri, *, open_timeout=None, close_timeout=None,
                                 max_size=None, proxy=None, **kwargs):
            raise AssertionError("must not connect")
        module = types.SimpleNamespace(connect=incompatible_connect)
        self.assertEqual(CLIENT.detect_websocket_client(
            lambda name: object(), lambda name: module), "INCOMPATIBLE")

    def test_output_contract_and_privacy(self):
        lines = CLIENT.success_lines("PYTHON_WEBSOCKETS")
        CLIENT.validate_output(lines)
        self.assertIn("REDIRECT_SUPPRESSION_CAPABILITY=PASS", lines)
        self.assertEqual(lines[-6:], ["RESULT=PASS", "ERROR_CODE=NONE", "FAILURE_STAGE=COMPLETE",
                                      "ROLLBACK_RECOMMENDED=FALSE", "PE4_0B2A=COMPLETE", "PE4_0B2B=NOT_STARTED"])
        for unsafe in (["DETAIL=secret"], ["ERROR_CODE=TOKEN"], ["ERROR_CODE=BAD"],
                       ["RESULT={PASS}"], ["RESULT=192.168.1.1"], ["DETAIL=ws://example.invalid"],
                       ['DETAIL={"type":"auth_ok","ha_version":"2026.8.1"}'],
                       ["DETAIL=Invalid access token or password"]):
            self.failure(lambda u=unsafe: CLIENT.validate_output(u), "PRIVACY_CONTRACT_VIOLATION", "PRIVACY_VALIDATION")

    def test_failure_contract(self):
        for code in CLIENT.ERROR_CODES:
            for stage in ("ENDPOINT",):
                CLIENT.validate_output(CLIENT.failure_lines(code, stage))

    def test_proxy_detection_does_not_expose_values(self):
        self.assertTrue(CLIENT.proxy_influence_present({"HTTP_PROXY": "sensitive"}))
        self.assertFalse(CLIENT.proxy_influence_present({"HTTP_PROXY": ""}))

    @mock.patch.object(CLIENT, "websockets_check")
    @mock.patch.object(CLIENT, "rest_check")
    @mock.patch.object(CLIENT, "acquire_token", return_value="top-secret")
    @mock.patch.object(CLIENT, "validate_terminal")
    @mock.patch.object(CLIENT, "validate_execution_host")
    @mock.patch.object(CLIENT, "proxy_influence_present", return_value=False)
    @mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKETS")
    @mock.patch.object(CLIENT, "parse_args")
    def test_run_sequence_and_no_secret_output(self, parse, dependency, proxy, target,
                                               terminal, prompt, rest, ws):
        parse.return_value = CLIENT.Arguments("nutandpihole", "jazofv1", "192.168.100.252", "192.168.100.251", 8123, "PI5_HA")
        events = []
        target.side_effect = lambda *args, **kwargs: events.append("target")
        proxy.side_effect = lambda *args, **kwargs: events.append("proxy") or False
        dependency.side_effect = lambda: events.append("dependency") or "PYTHON_WEBSOCKETS"
        terminal.side_effect = lambda *args: events.append("terminal")
        prompt.side_effect = lambda: events.append("prompt") or "top-secret"
        rest.side_effect = lambda token, **kwargs: events.append("rest")
        ws.side_effect = lambda token, **kwargs: events.append("ws")
        output = []
        self.assertEqual(CLIENT.run(ARGS, output.append), 0)
        self.assertEqual(events, ["target", "proxy", "dependency", "terminal",
                                  "prompt", "rest", "ws"])
        self.assertNotIn("top-secret", "\n".join(output))
        self.assertNotIn("Authorization", "\n".join(output))

    @mock.patch.object(CLIENT, "detect_websocket_client", return_value="INCOMPATIBLE")
    @mock.patch.object(CLIENT, "proxy_influence_present", return_value=False)
    @mock.patch.object(CLIENT, "validate_execution_host")
    @mock.patch.object(CLIENT, "parse_args")
    def test_dependency_failure_before_prompt(self, parse, target, proxy, dependency):
        parse.return_value = CLIENT.Arguments("nutandpihole", "jazofv1", "192.168.100.252", "192.168.100.251", 8123, "PI5_HA")
        with mock.patch.object(CLIENT, "acquire_token") as prompt:
            output = []
            self.assertEqual(CLIENT.run(ARGS, output.append), 1)
            prompt.assert_not_called()
        self.assertIn("ERROR_CODE=REDIRECT_SUPPRESSION_UNAVAILABLE", output)
        self.assertIn("FAILURE_STAGE=WEBSOCKET_API_COMPATIBILITY", output)

    @mock.patch.object(CLIENT, "websockets_check")
    @mock.patch.object(CLIENT, "rest_check", side_effect=CLIENT.ContractFailure("AUTHENTICATION_FAILED", "AUTHENTICATION"))
    @mock.patch.object(CLIENT, "acquire_token", return_value="secret")
    @mock.patch.object(CLIENT, "validate_terminal")
    @mock.patch.object(CLIENT, "validate_execution_host")
    @mock.patch.object(CLIENT, "proxy_influence_present", return_value=False)
    @mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKETS")
    @mock.patch.object(CLIENT, "parse_args")
    def test_rest_failure_stops_websocket(self, parse, dependency, proxy, target,
                                          terminal, prompt, rest, ws):
        parse.return_value = CLIENT.Arguments("nutandpihole", "jazofv1", "192.168.100.252", "192.168.100.251", 8123, "PI5_HA")
        self.assertEqual(CLIENT.run(ARGS, list().append), 1)
        ws.assert_not_called()

    def run_with_network_clock(self, *, precheck=0, prompt=0, rest=1, ws=1,
                               credential_failure=False):
        clock = [0.0]
        deadlines = []
        clock_events = []
        output = []
        def monotonic():
            clock_events.append(("clock", clock[0]))
            return clock[0]
        def validate(*args, **kwargs):
            clock[0] += precheck
        def acquire():
            clock[0] += prompt
            if credential_failure:
                raise CLIENT.ContractFailure("AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION")
            clock_events.append(("credential_return", clock[0]))
            return "synthetic-secret"
        def rest_check(token, *, deadline):
            deadlines.append(("rest", deadline))
            clock[0] += rest
        def websocket_check(token, *, deadline):
            deadlines.append(("ws", deadline))
            clock[0] += ws
        with mock.patch.object(CLIENT.time, "monotonic", side_effect=monotonic), \
             mock.patch.object(CLIENT, "validate_execution_host", side_effect=validate), \
             mock.patch.object(CLIENT, "local_ipv4_addresses", return_value=set()), \
             mock.patch.object(CLIENT, "current_operator", return_value="fixture"), \
             mock.patch.object(CLIENT, "proxy_influence_present", return_value=False), \
             mock.patch.object(CLIENT, "detect_websocket_client", return_value="PYTHON_WEBSOCKETS"), \
             mock.patch.object(CLIENT, "validate_terminal"), \
             mock.patch.object(CLIENT, "acquire_token", side_effect=acquire), \
             mock.patch.object(CLIENT, "rest_check", side_effect=rest_check) as rest_mock, \
             mock.patch.object(CLIENT, "websockets_check", side_effect=websocket_check) as ws_mock:
            rc = CLIENT.run(ARGS, output.append)
        return rc, output, deadlines, clock_events, rest_mock, ws_mock

    def test_slow_prompt_excluded_from_shared_network_deadline(self):
        rc, output, deadlines, events, _, _ = self.run_with_network_clock(prompt=21)
        self.assertEqual(rc, 0)
        self.assertEqual(events[:2], [("credential_return", 21.0), ("clock", 21.0)])
        self.assertEqual(deadlines, [("rest", 41.0), ("ws", 41.0)])
        self.assertEqual(output, CLIENT.success_lines("PYTHON_WEBSOCKETS"))
        self.assertNotIn("synthetic-secret", "\n".join(output))

    def test_local_prechecks_excluded_from_network_budget(self):
        rc, output, deadlines, events, _, _ = self.run_with_network_clock(precheck=60, prompt=21)
        self.assertEqual(rc, 0)
        self.assertEqual(events[:2], [("credential_return", 81.0), ("clock", 81.0)])
        self.assertEqual(deadlines, [("rest", 101.0), ("ws", 101.0)])
        self.assertIn("PE4_0B2B=NOT_STARTED", output)

    def test_credential_failure_has_no_network_clock_or_operations(self):
        rc, output, deadlines, events, rest, ws = self.run_with_network_clock(
            precheck=60, prompt=21, credential_failure=True)
        self.assertEqual(rc, 1)
        self.assertEqual(events, [])
        self.assertEqual(deadlines, [])
        rest.assert_not_called()
        ws.assert_not_called()
        self.assertEqual(output, CLIENT.failure_lines(
            "AUTHENTICATION_UNAVAILABLE", "CREDENTIAL_ACQUISITION", "PYTHON_WEBSOCKETS"))

    def test_network_elapsed_budget_exhaustion_before_and_after_websocket(self):
        for rest_seconds, ws_seconds, expected_calls in (
                (21, 0, ["rest"]), (10, 11, ["rest", "ws"])):
            with self.subTest(rest=rest_seconds, ws=ws_seconds):
                rc, output, deadlines, _, _, _ = self.run_with_network_clock(
                    prompt=21, rest=rest_seconds, ws=ws_seconds)
                self.assertEqual(rc, 1)
                self.assertEqual([name for name, _ in deadlines], expected_calls)
                self.assertTrue(all(deadline == 41.0 for _, deadline in deadlines))
                self.assertEqual(output, CLIENT.failure_lines(
                    "ENDPOINT_UNAVAILABLE", "WEBSOCKET_CAPABILITY", "PYTHON_WEBSOCKETS"))

    def test_remaining_connect_read_caps_and_expired_deadline_unchanged(self):
        self.assertEqual((CLIENT.CONNECT_TIMEOUT, CLIENT.READ_TIMEOUT, CLIENT.TOTAL_BUDGET),
                         (5.0, 10.0, 20.0))
        with mock.patch.object(CLIENT.time, "monotonic", return_value=100.0):
            self.assertEqual(CLIENT.remaining_timeout(120.0, CLIENT.CONNECT_TIMEOUT, "ENDPOINT"), 5.0)
            self.assertEqual(CLIENT.remaining_timeout(120.0, CLIENT.READ_TIMEOUT, "ENDPOINT"), 10.0)
            self.assertEqual(CLIENT.remaining_timeout(103.0, CLIENT.READ_TIMEOUT, "ENDPOINT"), 3.0)
            self.failure(lambda: CLIENT.remaining_timeout(100.0, CLIENT.CONNECT_TIMEOUT, "ENDPOINT"),
                         "ENDPOINT_UNAVAILABLE", "ENDPOINT")

    def test_source_contains_no_forbidden_ha_commands_or_persistence(self):
        source = PATH.read_text(encoding="utf-8")
        for forbidden in ("/api/states", "subscribe_events", "config/device_registry/list",
                          ".storage/", "sqlite3", "mkdtemp", "NamedTemporaryFile"):
            self.assertNotIn(forbidden, source)

    def test_pi5_local_execution_assumptions_are_absent(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertNotIn('EXPECTED_HOSTNAME = "a0d7b954-ssh"', source)
        self.assertNotIn('EXPECTED_OPERATOR = "root"', source)
        self.assertIn('EXPECTED_EXECUTION_IPV4 = "192.168.100.252"', source)
        self.assertIn('HA_IPV4 = "192.168.100.251"', source)
        self.assertIn('WS_URI = "ws://192.168.100.251:8123/api/websocket"', source)




class BoundaryCorrectionTests(unittest.TestCase):
    failure = ClientTests.failure
    """Real HTTP parsing over deterministic, deadline-controlled socket I/O."""
    class Socket:
        def __init__(self, clock, *, write_step=0, header_step=0, body_step=0,
                     body=b'{"message":"API running."}', interrupt=None):
            self.clock = clock
            self.write_step, self.header_step, self.body_step = write_step, header_step, body_step
            self.header = (b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                           b'Connection: close\r\nContent-Length: ' + str(len(body)).encode() + b'\r\n\r\n')
            self.data = self.header + body
            self.position, self.closed, self.close_calls = 0, False, 0
            self.timeouts, self.sent, self.interrupt = [], bytearray(), interrupt
        def settimeout(self, value): self.timeouts.append(value)
        def send(self, value):
            if self.interrupt == "write": raise KeyboardInterrupt("PRIVATE_SENTINEL")
            step = self.write_step
            if step >= self.timeouts[-1]:
                self.clock[0] += self.timeouts[-1]
                raise TimeoutError
            self.clock[0] += step
            self.sent.extend(value[:1]); return 1
        def recv_into(self, buffer):
            phase = "header" if self.position < len(self.header) else "body"
            if self.interrupt == phase: raise KeyboardInterrupt("PRIVATE_SENTINEL")
            step = self.header_step if phase == "header" else self.body_step
            if step >= self.timeouts[-1]:
                self.clock[0] += self.timeouts[-1]
                raise TimeoutError
            self.clock[0] += step
            if self.position == len(self.data): return 0
            buffer[0] = self.data[self.position]; self.position += 1; return 1
        def close(self): self.closed = True; self.close_calls += 1

    def transport_case(self, **kwargs):
        clock = [0.0]; sock = self.Socket(clock, **kwargs)
        with mock.patch.object(CLIENT.time, "monotonic", side_effect=lambda: clock[0]), \
             mock.patch.object(CLIENT.socket, "create_connection", return_value=sock) as connect:
            if any(kwargs.get(k, 0) for k in ("write_step", "header_step", "body_step")):
                self.failure(lambda: CLIENT.rest_check("synthetic", deadline=20),
                             "ENDPOINT_UNAVAILABLE", "ENDPOINT")
                self.assertLessEqual(clock[0], 20)
            else:
                CLIENT.rest_check("synthetic", deadline=20)
            connect.assert_called_once()
        self.assertTrue(sock.closed)
        self.assertEqual(sock.close_calls, 1)
        return sock

    def test_rest_slow_write_absolute_deadline(self): self.transport_case(write_step=.3)
    def test_rest_slow_header_absolute_deadline(self): self.transport_case(header_step=.3)
    def test_rest_slow_body_absolute_deadline(self): self.transport_case(body_step=1)
    def test_rest_inside_deadline_real_parser(self):
        sock = self.transport_case()
        self.assertEqual(bytes(sock.sent).count(b'GET /api/ HTTP/1.1'), 1)
        self.assertIn(b'Authorization: Bearer synthetic', sock.sent)
    def test_rest_stalled_connect(self):
        with mock.patch.object(CLIENT.time, "monotonic", return_value=0), \
             mock.patch.object(CLIENT.socket, "create_connection", side_effect=TimeoutError) as connect:
            self.failure(lambda: CLIENT.rest_check("synthetic", deadline=20),
                         "ENDPOINT_UNAVAILABLE", "ENDPOINT")
            self.assertEqual(connect.call_args.kwargs['timeout'], 5)
    def test_rest_exact_expiry_never_connects(self):
        with mock.patch.object(CLIENT.time, "monotonic", return_value=20), \
             mock.patch.object(CLIENT.socket, "create_connection") as connect:
            self.failure(lambda: CLIENT.rest_check("synthetic", deadline=20),
                         "ENDPOINT_UNAVAILABLE", "ENDPOINT")
            connect.assert_not_called()
    def test_rest_real_parser_oversize_cleanup(self):
        sock = self.Socket([0], body=b'x' * (CLIENT.MAX_MESSAGE + 1))
        with mock.patch.object(CLIENT.socket, "create_connection", return_value=sock):
            self.failure(lambda: CLIENT.rest_check("synthetic"), "RESPONSE_TOO_LARGE", "ENDPOINT")
        self.assertTrue(sock.closed); self.assertEqual(sock.close_calls, 1)

    def test_duplicate_members_all_auth_schemas(self):
        cases = [
            (CLIENT._parse_auth_required, '{"type":"event","type":"auth_required","ha_version":"x"}'),
            (CLIENT._parse_auth_required, '{"type":"auth_required","ha_version":"x","ha_version":"y"}'),
            (CLIENT._parse_auth_result, '{"type":"event","type":"auth_ok","ha_version":"x"}'),
            (CLIENT._parse_auth_result, '{"type":"auth_invalid","type":"auth_ok","ha_version":"x"}'),
            (CLIENT._parse_auth_result, '{"type":"auth_invalid","message":"x","message":"y"}'),
            (CLIENT._parse_auth_result, '{"type":"auth_ok","ha_version":{"x":1,"x":2}}'),
        ]
        for parser, raw in cases:
            with self.subTest(raw=raw):
                self.failure(lambda: parser(raw), "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
        connection = FakeConnection(FakeResponse(body=b'{"message":"wrong","message":"API running."}'))
        self.failure(lambda: CLIENT.rest_check("synthetic", lambda *a, **k: connection),
                     "UNEXPECTED_SCHEMA", "REST_CAPABILITY")
        self.assertTrue(connection.closed)

    def test_decoder_recursion_and_malformed_inputs(self):
        depth = 100
        while True:
            raw = '[' * depth + '0' + ']' * depth
            self.assertLessEqual(len(raw), CLIENT.MAX_MESSAGE)
            try: json.loads(raw)
            except RecursionError: break
            depth *= 2
        for raw in (raw, '{', b'\xff'):
            self.failure(lambda: CLIENT._parse_auth_required(raw),
                         "UNEXPECTED_SCHEMA", "WEBSOCKET_CAPABILITY")
            payload = raw.encode() if isinstance(raw, str) else raw
            connection = FakeConnection(FakeResponse(body=payload))
            self.failure(lambda: CLIENT.rest_check("synthetic", lambda *a, **k: connection),
                         "UNEXPECTED_SCHEMA", "REST_CAPABILITY")
            self.assertTrue(connection.closed)

    def test_both_expired_receives_never_create_coroutine(self):
        for second in (False, True):
            with self.subTest(second=second):
                clock = [0]
                ws = FakeWebSocket(['{"type":"auth_required","ha_version":"x"}'])
                ws.recv = mock.AsyncMock(wraps=ws.recv)
                async def enter():
                    if not second: clock[0] = 20
                    return ws
                async def send(value): clock[0] = 20
                ws.__class__ = type('ExpirySocket', (FakeWebSocket,), {'__aenter__': lambda self: enter()})
                ws.send = send
                def connect(uri, *, open_timeout, close_timeout, max_size, proxy, **kwargs): return ws
                connect.process_redirect = reject_redirect
                sock = mock.Mock()
                with warnings.catch_warnings(record=True) as caught, \
                     mock.patch.object(CLIENT.time, "monotonic", side_effect=lambda: clock[0]), \
                     mock.patch.object(CLIENT.socket, "create_connection", return_value=sock):
                    warnings.simplefilter('always')
                    self.failure(lambda: CLIENT.websockets_check('synthetic', 20, types.SimpleNamespace(connect=connect)),
                                 'ENDPOINT_UNAVAILABLE', 'WEBSOCKET_CAPABILITY')
                    import gc; gc.collect()
                self.assertEqual(ws.recv.call_count, int(second))
                self.assertFalse(any('never awaited' in str(w.message) for w in caught))
                self.assertTrue(ws.closed); sock.close.assert_called_once()

    def run_network(self, rest, websocket):
        output = []
        with mock.patch.object(CLIENT, 'validate_execution_host'), \
             mock.patch.object(CLIENT, 'local_ipv4_addresses', return_value=set()), \
             mock.patch.object(CLIENT, 'current_operator', return_value='fixture'), \
             mock.patch.dict(CLIENT.os.environ, {}, clear=True), \
             mock.patch.object(CLIENT, 'detect_websocket_client', return_value='PYTHON_WEBSOCKETS'), \
             mock.patch.object(CLIENT, 'validate_terminal'), \
             mock.patch.object(CLIENT, 'acquire_token', return_value='PRIVATE_SYNTHETIC_TOKEN'), \
             mock.patch.object(CLIENT, 'rest_check', side_effect=rest), \
             mock.patch.object(CLIENT, 'websockets_check', side_effect=websocket) as ws:
            rc = CLIENT.run(ARGS, output.append)
        return rc, output, ws

    def test_rest_interrupt_real_transport_cleanup_and_rc130(self):
        original = CLIENT.rest_check
        for phase in ('connect', 'write', 'header', 'body'):
            sock = self.Socket([0], interrupt=phase)
            def rest(token, deadline): return original(token, deadline=deadline)
            effect = KeyboardInterrupt('PRIVATE_SENTINEL') if phase == 'connect' else None
            with mock.patch.object(CLIENT.socket, 'create_connection', return_value=sock, side_effect=effect):
                rc, output, ws = self.run_network(rest, mock.Mock())
            self.assertEqual(rc, 130); ws.assert_not_called()
            self.assertIn('FAILURE_STAGE=ENDPOINT', output)
            self.assertIn('PE4_0B2B=NOT_STARTED', output)
            self.assertNotIn('PRIVATE', '\n'.join(output)); CLIENT.validate_output(output)
            if phase != 'connect': self.assertTrue(sock.closed)

    def test_websocket_interrupt_cleanup_and_rc130(self):
        import contextlib
        import gc
        original = CLIENT.websockets_check
        for phase in ('connect', 'receive', 'send'):
            with self.subTest(phase=phase):
                sock = mock.Mock()
                ws = FakeWebSocket(['{"type":"auth_required","ha_version":"x"}'])
                tasks = []
                async def recv(): raise KeyboardInterrupt('PRIVATE_SENTINEL')
                async def send(value):
                    tasks.append(asyncio.current_task())
                    raise KeyboardInterrupt('PRIVATE_SENTINEL')
                if phase == 'receive': ws.recv = recv
                if phase == 'send': ws.send = send
                def connect(uri, *, open_timeout, close_timeout, max_size, proxy, **kwargs):
                    if phase == 'connect': raise KeyboardInterrupt('PRIVATE_SENTINEL')
                    return ws
                connect.process_redirect = reject_redirect
                def websocket(token, deadline):
                    return original(token, deadline, types.SimpleNamespace(connect=connect))
                stderr = io.StringIO()
                with mock.patch.object(CLIENT.socket, 'create_connection', return_value=sock), \
                     contextlib.redirect_stderr(stderr):
                    rc, output, _ = self.run_network(lambda *a, **k: None, websocket)
                    self.assertTrue(all(task.done() for task in tasks))
                    tasks.clear()
                    gc.collect()
                self.assertEqual(stderr.getvalue(), '')
                self.assertEqual(rc, 130); sock.close.assert_called_once()
                if phase != 'connect': self.assertTrue(ws.closed)
                self.assertIn('FAILURE_STAGE=WEBSOCKET_CAPABILITY', output)
                self.assertIn('PE4_0B2B=NOT_STARTED', output)
                self.assertNotIn('PRIVATE', '\n'.join(output)); CLIENT.validate_output(output)

    def test_network_system_exit_propagates(self):
        with self.assertRaises(SystemExit):
            self.run_network(SystemExit(7), mock.Mock())


if __name__ == "__main__":
    unittest.main()
