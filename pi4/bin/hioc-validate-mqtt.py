#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


HIOC_HOME = Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.config import load_config


JSON_TOPIC_SUFFIXES = (
    "incidents/active",
    "incidents/history",
    "incidents/summary",
    "timeline/history",
    "timeline/latest",
    "status/detail",
)
TOPIC_SUFFIXES = JSON_TOPIC_SUFFIXES + ("status",)


@dataclass(frozen=True)
class TopicResult:
    topic: str
    status: str
    detail: str


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Read-only validation of HIOC retained Incident Engine MQTT topics."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Maximum seconds allowed for each retained-topic read (default: 5).",
    )
    return parser.parse_args(argv)


def resolve_settings(config):
    host = str(config.get("MQTT_HOST", "")).strip()
    if not host:
        raise ValueError("MQTT_HOST is not configured")
    try:
        port = int(str(config.get("MQTT_PORT", "1883")).strip())
    except ValueError as exc:
        raise ValueError("MQTT_PORT is not a valid integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("MQTT_PORT must be between 1 and 65535")
    base = str(config.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")).strip().strip("/")
    if not base:
        raise ValueError("HIOC_BASE_TOPIC is not configured")
    return {
        "host": host,
        "port": port,
        "user": str(config.get("MQTT_USER", "")),
        "password": str(config.get("MQTT_PASSWORD", "")),
        "base_topic": base,
    }


def subscriber_command(settings, topic):
    command = [
        "mosquitto_sub",
        "-h",
        settings["host"],
        "-p",
        str(settings["port"]),
        "-C",
        "1",
        "-t",
        topic,
    ]
    if settings["user"]:
        command.extend(["-u", settings["user"]])
    if settings["password"]:
        command.extend(["-P", settings["password"]])
    return command


def safe_error(value, settings):
    text = str(value).strip() or "subscriber returned no diagnostic"
    for secret in (settings["password"], settings["user"]):
        if secret:
            text = text.replace(secret, "[redacted]")
    return " ".join(text.splitlines())


def retained_payload(stdout):
    if stdout.endswith(b"\n"):
        stdout = stdout[:-1]
        if stdout.endswith(b"\r"):
            stdout = stdout[:-1]
    return stdout


def read_retained(settings, topic, timeout):
    try:
        completed = subprocess.run(
            subscriber_command(settings, topic),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError:
        return "FAIL", None, "mosquitto_sub is not installed"
    except subprocess.TimeoutExpired:
        return "INCOMPLETE", None, f"no retained payload received within {timeout:g}s"
    except OSError as exc:
        return "FAIL", None, safe_error(exc, settings)
    if completed.returncode != 0:
        return (
            "FAIL",
            None,
            f"mosquitto_sub exited {completed.returncode}: "
            f"{safe_error(completed.stderr.decode(errors='replace'), settings)}",
        )
    payload = retained_payload(completed.stdout)
    if not payload:
        return "FAIL", None, "retained payload is empty"
    return "PASS", payload, ""


def summarize_payload(topic, payload):
    fields = [f"bytes={len(payload)}"]
    if topic.endswith("/status"):
        try:
            status = payload.decode("utf-8")
        except UnicodeDecodeError:
            return "FAIL", " ".join(fields + ["utf8=invalid"])
        if status != "online":
            return "FAIL", " ".join(fields + [f"status={status!r}"])
        return "PASS", " ".join(fields + ["status=online"])

    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError:
        return "FAIL", " ".join(fields + ["json=invalid", "reason=invalid-utf8"])
    try:
        value = json.loads(decoded)
    except json.JSONDecodeError as exc:
        return (
            "FAIL",
            " ".join(
                fields
                + [
                    "json=invalid",
                    f"reason=line-{exc.lineno}-column-{exc.colno}",
                ]
            ),
        )
    fields.append("json=valid")
    if topic.endswith("/incidents/history"):
        if isinstance(value, list):
            fields.append(f"records={len(value)}")
            review_present = any(
                isinstance(record, dict) and bool(record.get("review"))
                for record in value
            )
            fields.append(f"embedded_review={'yes' if review_present else 'no'}")
            if value and not review_present:
                return "WARNING", " ".join(fields)
        else:
            fields.extend(["records=unsupported-structure", "embedded_review=unknown"])
            return "WARNING", " ".join(fields)
    return "PASS", " ".join(fields)


def validate(config, timeout):
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    settings = resolve_settings(config)
    topics = [f"{settings['base_topic']}/{suffix}" for suffix in TOPIC_SUFFIXES]
    results = []
    for topic in topics:
        read_status, payload, detail = read_retained(settings, topic, timeout)
        if read_status != "PASS":
            results.append(TopicResult(topic, read_status, detail))
            continue
        payload_status, payload_detail = summarize_payload(topic, payload)
        results.append(TopicResult(topic, payload_status, payload_detail))
    return settings, results


def overall_status(results):
    statuses = {result.status for result in results}
    if "FAIL" in statuses:
        return "FAIL", 1
    if "INCOMPLETE" in statuses:
        return "INCOMPLETE", 2
    return "PASS", 0


def main(argv=None):
    args = parse_args(argv)
    print(
        "MQTT VALIDATION | PURPOSE | read-only retained Incident Engine contract"
    )
    try:
        settings, results = validate(load_config(), args.timeout)
    except ValueError as exc:
        print(f"MQTT VALIDATION | CONFIG | FAIL | {exc}")
        print("MQTT VALIDATION | RESULT | FAIL")
        return 1

    print(
        "MQTT VALIDATION | ENDPOINT | "
        f"{settings['host']}:{settings['port']} | "
        f"authentication={'configured' if settings['user'] or settings['password'] else 'not-configured'}"
    )
    for result in results:
        print(
            f"MQTT VALIDATION | TOPIC | {result.topic} | "
            f"{result.status} | {result.detail}"
        )
    status, exit_code = overall_status(results)
    successful_reads = sum(
        result.status in {"PASS", "WARNING"} for result in results
    )
    if successful_reads:
        connectivity = "PASS"
    elif any(result.status == "FAIL" for result in results):
        connectivity = "FAIL"
    else:
        connectivity = "INCOMPLETE"
    print(f"MQTT VALIDATION | CONNECTIVITY | {connectivity}")
    print(f"MQTT VALIDATION | RESULT | {status}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
