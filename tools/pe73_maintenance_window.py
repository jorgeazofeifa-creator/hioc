"""Bounded PE-7.3 maintenance-window provider. Native mutation needs explicit TTY authority.

Interactive per-operation authority; no automatic recovery, process killing, service control or universal exclusion.
MaintenanceCoordinator binds explicit decisions to fresh observations; no input receipt unlocks mutation.
The accepted Controller transaction methods and strict core journal validator are reused.
"""
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import json
import os
import posixpath
from pathlib import Path
import re
import socket
import stat
import sys
import subprocess
import time
import uuid

PIN = "76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2"
path = Path(__file__).with_name("hioc-pe73-pi3-delivery.py")
if hashlib.sha256(path.read_bytes()).hexdigest() != PIN:
    raise RuntimeError("ACCEPTED_CONTROLLER_CHANGED")
spec = importlib.util.spec_from_file_location("pe73_window_core", path)
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
require = d.require
BACKUP = d.TX + "/window-crontab-original"
RISKS = ["INDEPENDENT_CALLER", "MISSED_PROCESS", "CACHED_MODULE", "RETAINED_DESCRIPTOR",
         "ALTERNATE_LAUNCHER", "CONCURRENT_SCHEDULER_EDITOR"]
ACTIONS = {"PRESERVE", "EXCLUDE", "DRAIN", "ESTABLISH", "ATTACH", "COMMIT", "ROLLBACK",
           "AUTHORIZE_RELEASE", "RESTORE_SCHEDULER", "RELEASE"}
SCHEDULER_OPERATION_PIN = "8c7026ba84b748677381ea9adfef9334156795eabb16df059a2e752a90049e66"

DEPLOYMENT_SEQUENCE = ("PREPARE", "PRESERVE", "EXCLUDE", "DRAIN", "ESTABLISH", "COMMIT",
                       "AUTHORIZE_RELEASE", "RESTORE_SCHEDULER", "RELEASE")
OPERATION_IMPACTS = {
    "PREPARE": "Save five original files and prepare thirteen verified delivery files. No live runtime file is replaced.",
    "PRESERVE": "Save the exact current schedule for later verified restoration. Scheduled jobs are not changed.",
    "EXCLUDE": "Temporarily pause the three approved HIOC scheduled jobs. Preserve the other nine entries.",
    "DRAIN": "Check that no known affected process is running and record the observation. Do not stop or kill processes.",
    "ESTABLISH": "Recheck the schedule and known processes, then record that this maintenance window is ready.",
    "COMMIT": "Install the thirteen verified files in dependency order and verify them. Do not activate PE-7 features.",
    "AUTHORIZE_RELEASE": "Authorize reopening only after the complete installation or authorized rollback has been verified. This step does not restore the schedule.",
    "RESTORE_SCHEDULER": "Restore and verify the exact original schedule. The three paused HIOC jobs can run again.",
    "RELEASE": "Finish the verified window and end the restriction on independent or manual affected commands.",
    "ATTACH": "Inspect an existing transaction and bind a fresh recovery session. Do not resume or adopt uncertain changes.",
    "ROLLBACK": "Perform the separately authorized rollback using verified original-file backups and exact installed-file provenance.",
}
OPERATOR_NOTICE = (
    "PI3 NUT&PIHOLE - operator jazofv1. Approve this step only.\n"
    "You must control this window alone. Do not run independent or manual affected commands until release is confirmed.\n"
    "A known process may be missed; cached modules, retained file descriptors, alternate launchers and concurrent schedule edits remain risks. Manual restrictions are procedural, not universal technical exclusion.\n"
    "N, blank or invalid input stops. Stopping never automatically retries, rolls back, restores the schedule or releases callers. Keep the manual restriction until explicit release.\n"
)

PHASES = {"PRESERVATION_UNCERTAIN", "PRESERVED", "EXCLUSION_UNCERTAIN", "EXCLUDED",
          "DRAINED", "ESTABLISHED", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
          "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED", "RELEASE_AUTHORIZED",
          "RESTORE_UNCERTAIN", "SCHEDULER_RESTORED", "RELEASED"}


def process_evidence(v):
    require(type(v) is dict and set(v) == {"boot_id", "observed_at", "known_active",
        "inspection_complete", "limitations", "universal_exclusion"}, "PROCESS_EVIDENCE_INVALID")
    require(type(v["boot_id"]) is str and d.AUTH.fullmatch(v["boot_id"]) and
        type(v["observed_at"]) is int and v["observed_at"] >= 0 and
        type(v["inspection_complete"]) is bool and v["universal_exclusion"] is False,
        "PROCESS_EVIDENCE_INVALID")
    require(type(v["known_active"]) is list and len(v["known_active"]) <= 4096 and
        type(v["limitations"]) is list and len(v["limitations"]) <= 4096 and
        all(type(x) is str and 0 < len(x) <= 128 for x in v["limitations"]), "PROCESS_EVIDENCE_INVALID")
    for item in v["known_active"]:
        require(type(item) is dict and set(item) == {"pid", "start_ticks", "command_sha256"} and
            type(item["pid"]) is int and item["pid"] > 0 and type(item["start_ticks"]) is int and
            item["start_ticks"] >= 0 and type(item["command_sha256"]) is str and
            d.DIGEST.fullmatch(item["command_sha256"]), "PROCESS_EVIDENCE_INVALID")
    return v


# Source-observed HIOC entry points, not a claim that each is active on PI3.
RUNTIME_BIN = "/home/jazofv1/hioc/pi4/bin"
ENTRY_NAMES = frozenset({"hioc-assets.py", "hioc-classify-metadata.py", "hioc-validate-assets.py",
    "hioc-availability-adapter.py", "hioc-inventory-engine.py", "hioc-platform-status.py",
    "hioc-incident-engine-v2.py", "hioc-history-engine.py", "hioc-resolve-local-services.py",
    "hioc-compose-service-associations.py", "hioc-install-mqtt-mappings.py",
    "hioc-home-assistant-association.py", "hioc-validate-mqtt.py", "hioc-validate-enrichment.py",
    "hioc-generate-manufacturer.py", "hioc-build-manufacturer-db.py", "hioc-validate-manufacturer.py"})
ENTRY_PATHS = frozenset(RUNTIME_BIN + "/" + name for name in ENTRY_NAMES)


def invocation(tokens):
    """Parse fixed CPython script/options grammar; never execute or shell-split argv."""
    if not tokens:
        return "NONE", ""
    executable = posixpath.basename(tokens[0])
    if executable in ENTRY_NAMES:
        return "SCRIPT", tokens[0]
    if not re.fullmatch(r"python(?:[0-9]+(?:[.][0-9]+)*)?d?", executable):
        return "NONE", ""
    i = 1
    while i < len(tokens):
        arg = tokens[i]
        if arg == "--":
            return ("SCRIPT", tokens[i+1]) if i+1 < len(tokens) else ("NONE", "")
        if arg in {"-c", "-m"}:
            return ("CODE" if arg == "-c" else "MODULE", tokens[i+1]) if i+1 < len(tokens) else ("AMBIGUOUS", "")
        if arg.startswith("-c") and len(arg)>2:
            return "CODE", arg[2:]
        if arg.startswith("-m") and len(arg)>2:
            return "MODULE", arg[2:]
        if arg in {"-W", "-X", "--check-hash-based-pycs"}:
            if i+1 >= len(tokens):
                return "AMBIGUOUS", ""
            i += 2
            continue
        if arg.startswith(("-W", "-X", "--check-hash-based-pycs=")):
            i += 1
            continue
        if arg in {"--help", "--help-env", "--help-xoptions", "--help-all", "--version"}:
            return "NONE", ""
        if arg.startswith("-") and arg != "-":
            if len(arg)>1 and set(arg[1:]) <= set("bBdEhiIOPqRsSuvVx"):
                if "h" in arg or "V" in arg:
                    return "NONE", ""
                i += 1
                continue
            return "AMBIGUOUS", ""
        return ("NONE", "") if arg == "-" else ("SCRIPT", arg)
    return "NONE", ""


def potential_relative(kind, script, tokens):
    if kind == "SCRIPT":
        return not posixpath.isabs(script) and posixpath.basename(script) in ENTRY_NAMES
    return kind == "AMBIGUOUS" and any(posixpath.basename(t) in ENTRY_NAMES for t in tokens[1:])


def cwd_target(cwd, script):
    # Kernel cwd links resolve the directory, but lexical '..' or script aliases
    # cannot safely be resolved here through the observer's potentially different view.
    if type(cwd) is not str or not posixpath.isabs(cwd) or cwd.endswith(" (deleted)") or ".." in script.split("/"):
        raise ValueError("AMBIGUOUS_CWD_TARGET")
    result = posixpath.normpath(posixpath.join(cwd, script))
    if result not in ENTRY_PATHS:
        raise ValueError("POTENTIALLY_AFFECTED_ALIAS_UNRESOLVED")
    return result


class NativeOps:
    """Fixed native operations admitted only by a fresh, context-bound technical grant."""
    def __init__(self):
        self.boot_id = self.target_boot()
    def target_boot(self):
        require(os.name == "posix" and sys.platform == "linux" and socket.gethostname() == "nutandpihole" and
            os.getuid() == os.geteuid() == os.getgid() == os.getegid() == 1000, "TARGET_IDENTITY")
        boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        require(d.AUTH.fullmatch(boot), "BOOT_ID_UNAVAILABLE")
        return boot
    def now(self):
        return int(time.time())
    def scheduler(self):
        # Fixed argv/environment, no shell or private stderr in receipts.
        result = subprocess.run(["/usr/bin/crontab", "-l"], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
            env={"PATH": "/usr/bin:/bin", "LANG": "C"})
        require(result.returncode == 0 and 0 < len(result.stdout) <= 65536,
            "SCHEDULER_OBSERVATION_FAILED")
        return result.stdout
    def live_gate(self):
        a = getattr(self, "_admission", None)
        require(type(a) is _NativeAdmission and a.ops is self and a.pid == os.getpid(),
                "NATIVE_WINDOW_ACCEPTANCE_REQUIRED")
        require(self.target_boot() == a.boot_id == self.boot_id and
            self.now() < a.expires_at and time.monotonic() < a.monotonic_deadline,
            "NATIVE_WINDOW_CONTEXT_EXPIRED_OR_CHANGED")
    def scheduler_gate(self):
        a = getattr(self, "_admission", None)
        require(type(a) is _NativeAdmission and a.action in {"EXCLUDE", "RESTORE_SCHEDULER"},
                "NATIVE_SCHEDULER_NOT_QUALIFIED")
        self.live_gate()
        operation = (inspect.getsource(NativeOps.scheduler) + "\n" + inspect.getsource(NativeOps.install_scheduler)).encode()
        require(d.sha(operation) == SCHEDULER_OPERATION_PIN, "SCHEDULER_QUALIFIED_OPERATION_CHANGED")
        value = a.coordinator.controller._journal()
        w = value.get("window")
        phase = "EXCLUSION_UNCERTAIN" if a.action == "EXCLUDE" else "RESTORE_UNCERTAIN"
        require(w is not None and w["phase"] == phase and w["session"] == a.coordinator.provider.session and
            w["boot_id"] == self.boot_id and w["authorizations"][-1]["action"] == a.action and
            w["authorizations"][-1]["reference"] == a.reference and not a.scheduler_attempted,
            "SCHEDULER_DURABLE_AUTHORIZATION_REQUIRED")
        a.scheduler_attempted = True  # Even an uncertain command is never retried.
    def install_scheduler(self, raw, expected_sha):
        self.scheduler_gate()
        self.live_gate()
        require(type(raw) is bytes and 0 < len(raw) <= 65536 and
            type(expected_sha) is str and d.DIGEST.fullmatch(expected_sha), "SCHEDULER_INPUT_INVALID")
        require(d.sha(self.scheduler()) == expected_sha, "WINDOW_SCHEDULER_DRIFT")
        # Single attempt. Nonzero exit/timeout/verification failure is uncertain;
        # the caller already persisted EXCLUSION_UNCERTAIN or RESTORE_UNCERTAIN.
        result = subprocess.run(["/usr/bin/crontab", "-"], input=raw,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
            env={"PATH": "/usr/bin:/bin", "LANG": "C"})
        require(result.returncode == 0, "SCHEDULER_INSTALL_UNCONFIRMED")
        require(self.scheduler() == raw, "SCHEDULER_INSTALL_UNCONFIRMED")
    def processes(self):
        active, limitations = [], []
        entries = [p for p in Path("/proc").iterdir() if p.name.isdecimal()]
        require(len(entries) <= 4096, "PROCESS_SCAN_LIMIT")
        complete = True
        for p in entries:
            if int(p.name) == os.getpid():
                continue
            potential = False
            try:
                proc_before = p.stat()
                stat_before = (p / "stat").read_text()
                with (p / "cmdline").open("rb") as stream:
                    raw = stream.read(65537)
                require(len(raw) <= 65536, "PROCESS_SCAN_LIMIT")
                byte_tokens = raw.split(b"\0")
                tokens = [os.fsdecode(t) for t in (byte_tokens[:-1] if byte_tokens[-1] == b"" else byte_tokens)]
                kind, script = invocation(tokens)
                potential = potential_relative(kind, script, tokens)
                known = any(b"/home/jazofv1/hioc/" in t or b"from hioc" in t or
                    b"import hioc" in t for t in byte_tokens)
                if kind == "MODULE" and (script == "hioc" or script.startswith("hioc.")):
                    known = True
                cwd_before = None
                if potential:
                    if kind == "AMBIGUOUS":
                        raise ValueError("AMBIGUOUS_PYTHON_ARGUMENTS")
                    cwd_before = os.readlink(p / "cwd")
                    cwd_target(cwd_before, script)
                    known = True
                # Bind argv/cwd observations to a stable PID directory and start identity.
                with (p / "cmdline").open("rb") as stream:
                    raw_after = stream.read(65537)
                cwd_after = os.readlink(p / "cwd") if potential else None
                stat_raw = (p / "stat").read_text()
                proc_after = p.stat()
                start = int(stat_raw.rsplit(")", 1)[1].split()[19])
                if (start != int(stat_before.rsplit(")", 1)[1].split()[19])
                        or (proc_before.st_dev, proc_before.st_ino) != (proc_after.st_dev, proc_after.st_ino)
                        or raw_after != raw or cwd_before != cwd_after):
                    complete = False
                    limitations.append("PROCESS_IDENTITY_OR_ARGUMENT_DRIFT_PID_" + p.name)
                    continue
                if known:
                    active.append({"pid": int(p.name), "start_ticks": start,
                        "command_sha256": d.sha(raw)})
                elif raw:
                    limitations.append("UNCLASSIFIED_PID_" + p.name)
            except FileNotFoundError:
                if potential:
                    complete = False
                limitations.append("VANISHED_PID_" + p.name)
            except (OSError, ValueError, IndexError):
                complete = False
                limitations.append("INCOMPLETE_PROCESS_CLASSIFICATION_PID_" + p.name)
        limitations.append("CACHED_MODULES_AND_RETAINED_DESCRIPTORS_NOT_UNIVERSALLY_OBSERVABLE")
        return process_evidence({"boot_id": self.boot_id, "observed_at": self.now(),
            "known_active": active, "inspection_complete": complete,
            "limitations": limitations, "universal_exclusion": False})


class _CoreView:
    """Read-only projection for the UNCHANGED strict core validator, never disk mutation."""
    def __init__(self, fs, core):
        self.fs, self.core = fs, core
    def read(self, path, mode=0o600):
        return d.canonical(self.core) if path == d.TX + "/journal.json" else self.fs.read(path, mode)


def validate_window(fs, value):
    w = value["window"]
    require(type(w) is dict and set(w) == {"version", "kind", "phase", "original_sha256",
        "reduced_sha256", "approved_jobs", "inventory", "operator", "boot_id", "session",
        "drain", "authorizations", "release_runtime_sha256"}, "WINDOW_JOURNAL_INVALID")
    require(type(w["version"]) is int and w["version"] == 1 and
        w["kind"] == "SCHEDULED_TECHNICAL_MANUAL_PROCEDURAL" and w["phase"] in PHASES,
        "WINDOW_JOURNAL_INVALID")
    for k in ("original_sha256", "reduced_sha256"):
        require(type(w[k]) is str and d.DIGEST.fullmatch(w[k]), "WINDOW_JOURNAL_INVALID")
    for k in ("operator", "boot_id", "session"):
        require(type(w[k]) is str and d.AUTH.fullmatch(w[k]), "WINDOW_JOURNAL_INVALID")
    if w["phase"] != "PRESERVATION_UNCERTAIN":
        raw = fs.read(BACKUP)
        require(d.sha(raw) == w["original_sha256"] and
            d.sha(d.maintenance_cron(raw, w["approved_jobs"], w["inventory"])) == w["reduced_sha256"],
            "WINDOW_BACKUP_INVALID")
    else:
        require(type(w["approved_jobs"]) is list and type(w["inventory"]) is dict,
            "WINDOW_JOURNAL_INVALID")
    refs = []
    require(type(w["authorizations"]) is list and 1 <= len(w["authorizations"]) <= 64,
        "WINDOW_JOURNAL_INVALID")
    for a in w["authorizations"]:
        require(type(a) is dict and set(a) == {"action", "reference", "grant_sha256"} and
            a["action"] in ACTIONS and type(a["reference"]) is str and d.AUTH.fullmatch(a["reference"]) and
            type(a["grant_sha256"]) is str and d.DIGEST.fullmatch(a["grant_sha256"]), "WINDOW_JOURNAL_INVALID")
        refs.append(a["reference"])
    require(len(set(refs)) == len(refs), "WINDOW_JOURNAL_INVALID")
    # Authorization history is ordered evidence, never just a phase label.
    stage = 0
    for event in w["authorizations"]:
        action = event["action"]
        if action == "ATTACH":
            require(1 <= stage <= 6, "WINDOW_AUTHORIZATION_ORDER")
        elif action == "DRAIN":
            require(2 <= stage <= 6, "WINDOW_AUTHORIZATION_ORDER")
            if stage == 2:
                stage = 3
        else:
            next_stage = {"PRESERVE": (0, 1), "EXCLUDE": (1, 2), "ESTABLISH": (3, 4),
                "AUTHORIZE_RELEASE": (4, 5), "RESTORE_SCHEDULER": (5, 6), "RELEASE": (6, 7)}
            require(action in next_stage and stage == next_stage[action][0], "WINDOW_AUTHORIZATION_ORDER")
            stage = next_stage[action][1]
    allowed = {1: {"PRESERVATION_UNCERTAIN", "PRESERVED"},
        2: {"EXCLUSION_UNCERTAIN", "EXCLUDED"}, 3: {"DRAINED"},
        4: {"ESTABLISHED", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
            "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED"},
        5: {"RELEASE_AUTHORIZED"}, 6: {"RESTORE_UNCERTAIN", "SCHEDULER_RESTORED"}, 7: {"RELEASED"}}
    require(w["phase"] in allowed.get(stage, set()), "WINDOW_AUTHORIZATION_ORDER")
    if w["drain"] is not None:
        b = process_evidence(w["drain"])
        require(b["inspection_complete"] and not b["known_active"], "WINDOW_DRAIN_INVALID")
    phase = w["phase"]
    if phase in {"PRESERVATION_UNCERTAIN", "PRESERVED", "EXCLUSION_UNCERTAIN", "EXCLUDED", "DRAINED", "ESTABLISHED"}:
        require(value["state"] == "PREPARED", "WINDOW_CORE_STATE")
    states = {"INSTALLATION_UNCERTAIN": "COMMITTING", "INSTALLATION_VERIFIED": "COMMITTED",
              "ROLLBACK_UNCERTAIN": "ROLLING_BACK", "RESTORATION_VERIFIED": "ROLLED_BACK"}
    if phase in states:
        require(value["state"] == states[phase], "WINDOW_CORE_STATE")
    release = {"RELEASE_AUTHORIZED", "RESTORE_UNCERTAIN", "SCHEDULER_RESTORED", "RELEASED"}
    require(w["release_runtime_sha256"] is None if phase not in release else
        type(w["release_runtime_sha256"]) is str and d.DIGEST.fullmatch(w["release_runtime_sha256"]),
        "WINDOW_RELEASE_INVALID")
    if phase in release:
        require(value["state"] in {"COMMITTED", "ROLLED_BACK"} and value["pending"] is None,
            "WINDOW_RELEASE_INVALID")


class WindowController(d.Controller):
    """Inherited prepare/commit/rollback algorithms; explicit extended journal envelope."""
    def prepare(self, reference, expected_preflight_sha):
        self.consumers.ops.live_gate()
        self.consumers._cron(original=True)
        return super().prepare(reference, expected_preflight_sha)
    def _validate(self, value):
        require(type(value) is dict and not ("window" in value and "maintenance" in value),
            "WINDOW_JOURNAL_INVALID")
        core = {k: v for k, v in value.items() if k != "window"}
        # Unknown core fields, snapshots, prefix/provenance and backups use original code.
        d.Controller(_CoreView(self.fs, core), self.source, self.consumers)._journal()
        if "window" in value:
            validate_window(self.fs, value)
        return value
    def _journal(self):
        try:
            return self._validate(d.parsed(self.fs.read(d.TX + "/journal.json")))
        except (KeyError, TypeError, AttributeError, IndexError, OverflowError):
            raise d.Failure("WINDOW_JOURNAL_INVALID") from None
    def _save(self, value, point):
        if "window" not in value:
            return super()._save(value, point)
        mapping = {"COMMITTING": "INSTALLATION_UNCERTAIN", "COMMITTED": "INSTALLATION_VERIFIED",
                   "ROLLING_BACK": "ROLLBACK_UNCERTAIN", "ROLLED_BACK": "RESTORATION_VERIFIED"}
        if point in mapping:
            value["window"]["phase"] = mapping[point]
        self._validate(value)
        self.fs.journal(value)
        self.fault(point)
    def commit(self, reference, expected_journal_sha):
        self.consumers.consume_runtime("COMMIT", reference, expected_journal_sha)
        return super().commit(reference, expected_journal_sha)
    def rollback(self, reference, expected_journal_sha):
        self.consumers.consume_runtime("ROLLBACK", reference, expected_journal_sha)
        return super().rollback(reference, expected_journal_sha)


class WindowConsumers:
    def __init__(self, ops, original, approved_jobs, inventory):
        self.ops, self.original = ops, original
        self.approved, self.inventory = copy.deepcopy(approved_jobs), copy.deepcopy(inventory)
        self.reduced = d.maintenance_cron(original, approved_jobs, inventory)
        self.session = uuid.uuid4().hex
        self.controller = None
        self.runtime_grant = None
        self.runtime_permit = False
        self.deadline = None
    def bind(self, fs, source):
        self.controller = WindowController(fs, source, self)
        return self.controller
    def observe(self):
        return {"cron_sha256": d.sha(self.original), "known_cron_commands": list(d.CRON),
            "coverage": "IDENTIFIED_SCHEDULER_ENTRIES_ONLY",
            "partial_failure_exclusion": "SCHEDULER_TECHNICAL_MANUAL_PROCEDURAL",
            "unlocked_asset_or_classification_callers": "PROCEDURALLY_PROHIBITED_NOT_ENFORCED"}
    def _load(self):
        require(self.controller is not None, "WINDOW_NOT_BOUND")
        return self.controller._journal()
    def _cron(self, original=False):
        require(self.ops.scheduler() == (self.original if original else self.reduced), "WINDOW_SCHEDULER_DRIFT")
    def _processes(self):
        b = process_evidence(self.ops.processes())
        require(b["boot_id"] == self.ops.boot_id and b["inspection_complete"] and not b["known_active"] and
            0 <= self.ops.now() - b["observed_at"] <= 30, "KNOWN_CONSUMERS_NOT_DRAINED")
        return b
    def _grant(self, grant, action, value):
        keys = {"action", "reference", "journal_sha256", "scheduler_sha256", "operator", "session",
                "boot_id", "expires_at", "exclusive_responsibility", "risks_acknowledged"}
        require(type(grant) is dict and set(grant) == keys and grant["action"] == action and
            type(grant["reference"]) is str and d.AUTH.fullmatch(grant["reference"]) and
            grant["journal_sha256"] == d.sha(d.canonical(value)) and
            grant["scheduler_sha256"] == d.sha(self.ops.scheduler()) and
            grant["session"] == self.session and grant["boot_id"] == self.ops.boot_id and
            type(grant["operator"]) is str and d.AUTH.fullmatch(grant["operator"]) and
            type(grant["expires_at"]) is int and 0 < grant["expires_at"] - self.ops.now() <= 3600 and
            grant["exclusive_responsibility"] is True and grant["risks_acknowledged"] == RISKS,
            "WINDOW_AUTHORIZATION_INVALID")
        w = value.get("window")
        used = [value[k] for k in ("prepare_authorization", "commit_authorization", "rollback_authorization")]
        if w:
            used += [a["reference"] for a in w["authorizations"]]
            require(grant["operator"] == w["operator"], "WINDOW_OPERATOR_MISMATCH")
        require(grant["reference"] not in used, "WINDOW_AUTHORIZATION_REUSED")
        self.deadline = grant["expires_at"]
        return {"action": action, "reference": grant["reference"], "grant_sha256": d.sha(d.canonical(grant))}
    def _record(self, value, event, phase):
        value["window"]["authorizations"].append(event)
        value["window"]["phase"] = phase
        self.controller._save(value, "WINDOW:" + phase)
    def progress(self, action, grant):
        require(action in ACTIONS - {"COMMIT", "ROLLBACK"}, "WINDOW_ACTION_INVALID")
        self.ops.live_gate()  # Native calls need the active scoped operation admission.
        with self.controller.fs.mutex():
            value = self._load()
            event = self._grant(grant, action, value)
            w = value.get("window")
            phase = w["phase"] if w else None
            if action == "PRESERVE":
                require(w is None and value["state"] == "PREPARED", "WINDOW_PHASE_REFUSED")
                self._cron(original=True)
                value["window"] = {"version": 1, "kind": "SCHEDULED_TECHNICAL_MANUAL_PROCEDURAL",
                    "phase": "PRESERVATION_UNCERTAIN", "original_sha256": d.sha(self.original),
                    "reduced_sha256": d.sha(self.reduced), "approved_jobs": self.approved,
                    "inventory": self.inventory, "operator": grant["operator"], "boot_id": self.ops.boot_id,
                    "session": self.session, "drain": None, "authorizations": [], "release_runtime_sha256": None}
                self._record(value, event, "PRESERVATION_UNCERTAIN")
                self.controller.fs.write_new(BACKUP, self.original)
                require(self.controller.fs.read(BACKUP) == self.original, "WINDOW_BACKUP_INVALID")
                self._cron(original=True)
                value["window"]["phase"] = "PRESERVED"
                self.controller._save(value, "WINDOW:PRESERVED")
            else:
                require(w is not None, "WINDOW_NOT_PRESERVED")
                require(w["original_sha256"] == d.sha(self.original) and w["reduced_sha256"] == d.sha(self.reduced)
                    and w["approved_jobs"] == self.approved and w["inventory"] == self.inventory,
                    "WINDOW_SCOPE_DRIFT")
                if action != "ATTACH":
                    require(w["session"] == self.session and w["boot_id"] == self.ops.boot_id, "WINDOW_REATTACH_REQUIRED")
                if action == "EXCLUDE":
                    require(phase == "PRESERVED", "WINDOW_PHASE_REFUSED")
                    self._cron(original=True)
                    self._record(value, event, "EXCLUSION_UNCERTAIN")
                    self.ops.install_scheduler(self.reduced, d.sha(self.original))
                    self._cron()
                    w["phase"] = "EXCLUDED"
                    self.controller._save(value, "WINDOW:EXCLUDED")
                elif action == "ATTACH":
                    require(phase not in {"PRESERVATION_UNCERTAIN", "EXCLUSION_UNCERTAIN", "RESTORE_UNCERTAIN", "RELEASED"}, "WINDOW_UNCERTAIN")
                    self._cron(original=phase == "SCHEDULER_RESTORED" or phase == "PRESERVED")
                    report = self.controller.inspect()
                    require(report["live_state_established"], "WINDOW_RUNTIME_UNCERTAIN")
                    w.update(session=self.session, boot_id=self.ops.boot_id, drain=None)
                    # Requalification never advances an artifact or scheduler phase.
                    self._record(value, event, phase)
                elif action == "DRAIN":
                    require(phase in {"EXCLUDED", "DRAINED", "ESTABLISHED", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
                        "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED", "RELEASE_AUTHORIZED", "SCHEDULER_RESTORED"}, "WINDOW_PHASE_REFUSED")
                    self._cron(original=phase == "SCHEDULER_RESTORED")
                    w["drain"] = self._processes()
                    self._record(value, event, "DRAINED" if phase in {"EXCLUDED", "DRAINED"} else phase)
                elif action == "ESTABLISH":
                    require(phase == "DRAINED" and w["drain"] is not None, "WINDOW_PHASE_REFUSED")
                    self._cron(); w["drain"] = self._processes()
                    self._record(value, event, "ESTABLISHED")
                elif action == "AUTHORIZE_RELEASE":
                    require(phase in {"INSTALLATION_VERIFIED", "RESTORATION_VERIFIED"}, "WINDOW_PHASE_REFUSED")
                    self.assert_active(); self._runtime(value)
                    w["release_runtime_sha256"] = self._runtime(value)
                    self._record(value, event, "RELEASE_AUTHORIZED")
                elif action == "RESTORE_SCHEDULER":
                    require(phase == "RELEASE_AUTHORIZED", "WINDOW_PHASE_REFUSED")
                    self._ready(value); self._cron()
                    require(self._runtime(value) == w["release_runtime_sha256"], "WINDOW_RUNTIME_DRIFT")
                    self._record(value, event, "RESTORE_UNCERTAIN")
                    self.ops.install_scheduler(self.original, d.sha(self.reduced))
                    self._cron(original=True)
                    w["phase"] = "SCHEDULER_RESTORED"
                    self.controller._save(value, "WINDOW:SCHEDULER_RESTORED")
                elif action == "RELEASE":
                    require(phase == "SCHEDULER_RESTORED", "WINDOW_PHASE_REFUSED")
                    self._ready(value); self._cron(original=True)
                    require(self._runtime(value) == w["release_runtime_sha256"], "WINDOW_RUNTIME_DRIFT")
                    self._record(value, event, "RELEASED")
            return self.inspect()
    def _runtime(self, value):
        d.check_sources(self.controller.source)
        require(value["state"] in {"COMMITTED", "ROLLED_BACK"} and value["pending"] is None and
            self.controller.inspect()["live_state_established"], "WINDOW_RUNTIME_UNCERTAIN")
        return d.sha(d.canonical({k: value[k] for k in ("state", "manifest_sha256", "baseline", "installed", "restored")}))
    def _ready(self, value):
        w = value["window"]
        require(w["original_sha256"] == d.sha(self.original) and w["reduced_sha256"] == d.sha(self.reduced)
            and w["approved_jobs"] == self.approved and w["inventory"] == self.inventory, "WINDOW_SCOPE_DRIFT")
        require(w["boot_id"] == self.ops.boot_id and w["session"] == self.session and
            w["drain"] is not None and self.deadline is not None and self.ops.now() < self.deadline,
            "WINDOW_FRESH_READINESS_REQUIRED")
        self._processes()
    def assert_active(self):
        self.ops.live_gate()
        value = self._load(); w = value.get("window")
        require(w is not None and w["phase"] in {"ESTABLISHED", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
            "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED"}, "WINDOW_NOT_ESTABLISHED")
        self._ready(value); self._cron()
    @contextlib.contextmanager
    def hold(self, observation):
        require(self.runtime_permit and observation == self.observe(), "WINDOW_RUNTIME_AUTHORIZATION_REQUIRED")
        self.assert_active()
        try:
            yield
        finally:
            self.runtime_permit = False  # Never restore scheduler or release consumers.
    def authorize_runtime(self, grant):
        require(grant.get("action") in {"COMMIT", "ROLLBACK"}, "WINDOW_ACTION_INVALID")
        self.ops.live_gate()
        value = self._load(); self._grant(grant, grant["action"], value)
        self.assert_active()
        self.runtime_grant = copy.deepcopy(grant)
    def consume_runtime(self, action, reference, binding):
        self.ops.live_gate()
        value = self._load(); grant, self.runtime_grant = self.runtime_grant, None
        require(grant is not None and grant["action"] == action and grant["reference"] == reference and
            binding == grant["journal_sha256"], "WINDOW_RUNTIME_AUTHORIZATION_REQUIRED")
        self._grant(grant, action, value); self.assert_active()
        self.runtime_permit = True
    def inspect(self):
        value = self._load(); w = value.get("window")
        native, admitted = isinstance(self.ops, NativeOps), False
        if native and type(getattr(self.ops, "_admission", None)) is _NativeAdmission:
            self.ops.live_gate()
            admitted = True
        operation = (inspect.getsource(NativeOps.scheduler) + "\n" + inspect.getsource(NativeOps.install_scheduler)).encode()
        return {"phase": w["phase"] if w else "NOT_ESTABLISHED", "journal_sha256": d.sha(d.canonical(value)),
            "scheduler_sha256": d.sha(self.ops.scheduler()), "process_observation": self.ops.processes(),
            "manual_launch_control": "PROCEDURAL_ONLY", "universal_exclusion": False,
            "native_qualified": native and d.sha(operation) == SCHEDULER_OPERATION_PIN,
            "native_qualification_scope": "ISOLATED_LINUX_SCHEDULER_OPERATION_ONLY",
            "production_authorized": admitted, "authorization_scope": "CURRENT_OPERATION_ONLY"}


class MaintenanceCoordinator:
    """One explicitly authorized operation, using the existing transaction/provider.

    Context digests bind decisions, not authenticate them. Native calls require
    an exact scoped admission, generated internally by the approved fixed process
    or by separately authorized out-of-scope intervention. Manual exclusion stays
    procedural. No retry or finally-based recovery is performed.
    """
    def __init__(self, provider, source_reader):
        self.provider = provider
        self.controller = provider.controller
        require(self.controller is not None and callable(source_reader), "WINDOW_NOT_BOUND")
        self.source_reader = source_reader

    @classmethod
    def native(cls, original, inventory):
        # Construction/inspection is read-only. Original bytes and the full
        # explicit inventory must be reviewed; do not invent production entries.
        ops = NativeOps()
        fs = d.NativeFS()
        source = d.source_gate()
        require(d.sha(original) == "3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9",
                "WINDOW_ORIGINAL_SCHEDULER_MISMATCH")
        provider = WindowConsumers(ops, original, list(d.CRON), inventory)
        require(d.sha(provider.reduced) == "443485cfb47920db8d6263e5266eb9f68811e81c06390a983a7006aac581b930",
                "WINDOW_REDUCED_SCHEDULER_MISMATCH")
        provider.bind(fs, source)
        return cls(provider, d.source_gate)

    def context(self, action):
        require(action == "PREPARE" or action in ACTIONS, "WINDOW_ACTION_INVALID")
        p, c = self.provider, self.controller
        fresh = self.source_reader()
        d.check_sources(fresh)
        require(fresh == c.source, "SOURCE_IDENTITY_MISMATCH")
        observed = process_evidence(p.ops.processes())
        require(observed["boot_id"] == p.ops.boot_id and
                0 <= p.ops.now() - observed["observed_at"] <= 30, "PROCESS_EVIDENCE_STALE")
        # The timestamp is checked for freshness, but advancing wall-clock time
        # alone must not invalidate an otherwise identical decision context.
        # Diagnostic unrelated PID churn is not authorization authority. Keep
        # freshness above, completeness, boot and exact affected-consumer evidence.
        # Incomplete/ambiguous classification still refuses; it is never excused
        # merely by calling a process unrelated.
        process = {k: observed[k] for k in ("boot_id", "inspection_complete", "universal_exclusion")}
        process["known_active"] = sorted(observed["known_active"],
            key=lambda item: (item["pid"], item["start_ticks"], item["command_sha256"]))
        scheduler = p.ops.scheduler()
        require(scheduler in (p.original, p.reduced), "WINDOW_SCHEDULER_DRIFT")
        runtime = {}
        for target in d.ORDER:
            snap = c.fs.snapshot(target)
            runtime[target] = c.fs.snapshot(target, d.MODES[target]) if snap["exists"] else snap
        if action == "PREPARE":
            require(not c.fs.transaction_present(), "TRANSACTION_EXISTS")
            evidence = d.preflight(c.fs, fresh, p)
            require(scheduler == p.original, "WINDOW_SCHEDULER_DRIFT")
            journal_sha, preflight_sha = None, d.sha(d.canonical(evidence))
        else:
            value = c._journal()
            journal_sha, preflight_sha = d.sha(d.canonical(value)), None
        return {"action": action, "release": d.RELEASE,
            "manifest_sha256": d.sha(d.canonical({"files": d.MANIFEST})),
            "controller_sha256": PIN, "runtime_sha256": d.sha(d.canonical(runtime)),
            "journal_sha256": journal_sha, "preflight_sha256": preflight_sha,
            "scheduler_sha256": d.sha(scheduler), "original_sha256": d.sha(p.original),
            "reduced_sha256": d.sha(p.reduced), "inventory_sha256": d.sha(d.canonical(p.inventory)),
            "approved_jobs": list(p.approved), "process_observation": process,
            "session": p.session, "boot_id": p.ops.boot_id,
            "manual_launch_control": "PROCEDURAL_ONLY", "universal_exclusion": False}

    def execute(self, action, authorization):
        p, c = self.provider, self.controller
        # A matching input dict alone is never native authority.
        p.ops.live_gate()
        if isinstance(p.ops, NativeOps):
            admission = p.ops._admission
            require(admission.coordinator is self and admission.action == action and
                admission.authorization_sha256 == d.sha(d.canonical(authorization)),
                "NATIVE_OPERATION_AUTHORIZATION_MISMATCH")
        current = self.context(action)
        keys = {"action", "context_sha256", "reference", "operator", "expires_at",
                "exclusive_responsibility", "risks_acknowledged"}
        a = authorization
        require(type(a) is dict and set(a) == keys and a["action"] == action and
            a["context_sha256"] == d.sha(d.canonical(current)) and
            type(a["reference"]) is str and d.AUTH.fullmatch(a["reference"]) and
            type(a["operator"]) is str and d.AUTH.fullmatch(a["operator"]) and
            type(a["expires_at"]) is int and 0 < a["expires_at"] - p.ops.now() <= 3600 and
            a["exclusive_responsibility"] is True and a["risks_acknowledged"] == RISKS,
            "COORDINATOR_AUTHORIZATION_INVALID")
        require(current["process_observation"]["inspection_complete"] and
                not current["process_observation"]["known_active"], "KNOWN_CONSUMERS_NOT_DRAINED")
        # Bind the durable authorization reference to the complete decision,
        # including its original external reference, without extending the journal.
        reference = "PE73_" + d.sha(d.canonical(a))
        if action == "PREPARE":
            return c.prepare(reference, current["preflight_sha256"])
        grant = {k: a[k] for k in ("operator", "expires_at", "exclusive_responsibility", "risks_acknowledged")}
        grant.update(action=action, reference=reference, journal_sha256=current["journal_sha256"],
            scheduler_sha256=current["scheduler_sha256"], session=p.session, boot_id=p.ops.boot_id)
        if action in {"COMMIT", "ROLLBACK"}:
            p.authorize_runtime(grant)
            return getattr(c, action.lower())(reference, current["journal_sha256"])
        return p.progress(action, grant)


    def interactive(self, action):
        """Native entry: one fresh named operator decision, never a receipt loader."""
        require(type(self.provider.ops) is NativeOps, "NATIVE_OPS_REQUIRED")
        require(action == "PREPARE" or action in ACTIONS, "WINDOW_ACTION_INVALID")
        reference = "AUTO_" + action + "_" + uuid.uuid4().hex
        ops = self.provider.ops
        require(getattr(ops, "_admission", None) is None, "NATIVE_OPERATION_ALREADY_ACTIVE")
        context = self.context(action)
        authorization = {"action": action, "context_sha256": d.sha(d.canonical(context)),
            "reference": reference, "operator": "UID1000_jazofv1", "expires_at": ops.now() + 300,
            "exclusive_responsibility": True, "risks_acknowledged": list(RISKS)}
        prompt = OPERATOR_NOTICE + OPERATION_IMPACTS[action] + "\nApprove this step? [Y/N]: "
        response = tty_line(prompt).strip().upper()
        require(response == "Y", "NATIVE_OPERATOR_AUTHORIZATION_REFUSED")
        require(self.context(action) == context and ops.now() < authorization["expires_at"],
                "NATIVE_AUTHORIZATION_CONTEXT_DRIFT")
        admission = _NativeAdmission(ops, self, action, authorization)
        ops._admission = admission
        try:
            return self.execute(action, authorization)
        finally:
            # Forget authority only. Never restore cron, roll back, or release.
            ops._admission = None


class _NativeAdmission:
    """Ephemeral internal authority; not serialized or accepted from operator JSON."""
    def __init__(self, ops, coordinator, action, authorization):
        self.ops, self.coordinator, self.action = ops, coordinator, action
        self.pid, self.boot_id = os.getpid(), ops.boot_id
        self.expires_at = authorization["expires_at"]
        self.monotonic_deadline = time.monotonic() + max(0, self.expires_at - ops.now())
        self.authorization_sha256 = d.sha(d.canonical(authorization))
        self.reference = "PE73_" + self.authorization_sha256
        self.scheduler_attempted = False


def tty_line(prompt):
    """Bounded controlling-terminal input, never stdin, an env var or input file."""
    fd = os.open("/dev/tty", os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NOCTTY)
    try:
        require(stat.S_ISCHR(os.fstat(fd).st_mode) and os.isatty(fd), "NATIVE_TTY_REQUIRED")
        # Drop prior/type-ahead responses. A queued Y must not approve a later operation.
        import termios
        termios.tcflush(fd, termios.TCIFLUSH)
        raw = prompt.encode("utf-8")
        while raw:
            written = os.write(fd, raw)
            require(written > 0, "NATIVE_TTY_WRITE_FAILED")
            raw = raw[written:]
        response = os.read(fd, 257)
        require(len(response) <= 256 and response.endswith(b"\n") and response.count(b"\n") == 1,
                "NATIVE_TTY_RESPONSE_INVALID")
        return response[:-1].decode("ascii", "strict")
    finally:
        os.close(fd)


def native_main():
    """Owner-approved fixed normal sequence; every technical operation guard remains."""
    ops = NativeOps()
    fs = d.NativeFS()
    current = ops.scheduler()
    original_sha = "3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9"
    original = current if d.sha(current) == original_sha else fs.read(BACKUP)
    # This exact hash and the reduced hash bind the full already-reviewed table.
    lines = original.decode("utf-8", "strict").splitlines()
    inventory = {line: "EXCLUDE" if line in d.CRON else "PRESERVE"
        for line in lines if line.strip() and not line.lstrip().startswith("#")}
    require(len(inventory) == 12 and list(inventory.values()).count("EXCLUDE") == 3,
            "WINDOW_SCHEDULER_INVENTORY_CHANGED")
    coordinator = MaintenanceCoordinator.native(original, inventory)
    run_deployment_sequence(coordinator)
    return 0


OWNER_SEQUENCE_AUTHORITY = "PE73_OWNER_SEQUENCE_AUTHORIZATION_20261027"
EXCLUDED_RECOVERY_JOURNAL_SHA256 = "b899a8fa79bde3c6619d6abd8217d88833c414823e7888358ed7a043b766600f"
RESUME_SEQUENCE = ("ATTACH", "DRAIN", "ESTABLISH", "COMMIT", "AUTHORIZE_RELEASE",
                   "RESTORE_SCHEDULER", "RELEASE")


def validate_excluded_resume(coordinator):
    """Read-only exact owner-supplied anchor; never adopt a label or edited receipt."""
    c, p = coordinator.controller, coordinator.provider
    raw = c.fs.read(d.TX + "/journal.json")
    require(d.sha(raw) == EXCLUDED_RECOVERY_JOURNAL_SHA256, "RECOVERY_JOURNAL_ANCHOR_MISMATCH")
    value = c._journal()
    w = value.get("window")
    require(value["state"] == "PREPARED" and value["pending"] is None and
        not value["installed"] and not value["restored"] and value["commit_authorization"] is None and
        value["rollback_authorization"] is None and w is not None and w["phase"] == "EXCLUDED" and
        w["drain"] is None and w["release_runtime_sha256"] is None and
        w["operator"] == "UID1000_jazofv1" and w["original_sha256"] == d.sha(p.original) and
        w["reduced_sha256"] == d.sha(p.reduced) and w["approved_jobs"] == p.approved and
        w["inventory"] == p.inventory, "RECOVERY_SCOPE_OR_PHASE_MISMATCH")
    p._cron()
    context = coordinator.context("ATTACH")
    require(context["process_observation"]["inspection_complete"] and
        not context["process_observation"]["known_active"], "KNOWN_CONSUMERS_NOT_DRAINED")
    require(c.inspect()["live_state_established"], "RECOVERY_RUNTIME_MISMATCH")
    # Existing secure reads validate owner/type/mode/ancestors. Verify all backup
    # and stage bytes BEFORE ATTACH writes its new session into the old journal.
    for index, target in enumerate(d.ORDER):
        require(c.fs.read(d.TX + "/stage-" + str(index)) == c.source[target], "STAGING_DRIFT")
        if target in d.PRIOR:
            require(d.sha(c.fs.read(d.TX + "/backup-" + str(index))) == value["baseline"][target]["sha256"],
                    "BACKUP_DRIFT")
    require(c.fs.read(d.TX + "/journal.json") == raw, "RECOVERY_JOURNAL_DRIFT")
    return d.sha(raw)


class _ApprovedSequence:
    """Owner-approved fixed process, not authority reconstructed from journal values.

    Never accepts a sequence, grant, approval flag or permission receipt as input.
    Only the normal fixed process or this exact separately approved EXCLUDED resume
    can enter. Every operation still creates a fresh technical grant and admission.
    """
    def __init__(self, coordinator, resume=False):
        require(type(resume) is bool, "SEQUENCE_ENTRY_INVALID")
        self.coordinator, self.resume = coordinator, resume
        self.actions = RESUME_SEQUENCE if resume else DEPLOYMENT_SEQUENCE
        self.index, self.stopped = 0, False
        self.pid = os.getpid()
        p = coordinator.provider
        self.boot_id, self.session = p.ops.boot_id, p.session
        self.expires_at = p.ops.now() + 3600
        self.monotonic_deadline = time.monotonic() + 3600
        if resume:
            self.expected_journal = validate_excluded_resume(coordinator)
        else:
            require(not coordinator.controller.fs.transaction_present(),
                    "EXISTING_TRANSACTION_REQUIRES_SEPARATE_RECOVERY")
            self.expected_journal = None
        initial = coordinator.context(self.actions[0])
        self.scope = {k: initial[k] for k in ("release", "manifest_sha256", "controller_sha256",
            "original_sha256", "reduced_sha256", "inventory_sha256", "approved_jobs")}
        self.reference = d.sha(d.canonical({"owner_authority": OWNER_SEQUENCE_AUTHORITY,
            "entry": "VERIFIED_EXCLUDED_RESUME" if resume else "NEW_NORMAL_DEPLOYMENT",
            "actions": list(self.actions), "initial_context": initial, "scope": self.scope,
            "journal_anchor": self.expected_journal, "nonce": uuid.uuid4().hex}))

    def perform_next(self):
        require(not self.stopped and self.index < len(self.actions), "SEQUENCE_STOPPED_OR_COMPLETE")
        p, c = self.coordinator.provider, self.coordinator.controller
        try:
            require(self.actions == (RESUME_SEQUENCE if self.resume else DEPLOYMENT_SEQUENCE),
                    "SEQUENCE_ACTION_SCOPE_DRIFT")
            require(os.getpid() == self.pid and p.session == self.session and p.ops.boot_id == self.boot_id and
                p.ops.now() < self.expires_at and time.monotonic() < self.monotonic_deadline,
                "SEQUENCE_FRESH_SESSION_REQUIRED")
            if self.expected_journal is None:
                require(not c.fs.transaction_present(), "TRANSACTION_EXISTS")
            else:
                require(d.sha(c.fs.read(d.TX + "/journal.json")) == self.expected_journal,
                        "SEQUENCE_JOURNAL_DRIFT")
                require(c.inspect()["live_state_established"], "SEQUENCE_RUNTIME_DRIFT")
            action = self.actions[self.index]
            context = self.coordinator.context(action)
            require({k: context[k] for k in self.scope} == self.scope, "SEQUENCE_SCOPE_DRIFT")
            if self.expected_journal is not None:
                value = c._journal(); window = value.get("window")
                original = window is None or window["phase"] in {"PRESERVED", "SCHEDULER_RESTORED"}
                p._cron(original=original)
                require(d.sha(c.fs.read(d.TX + "/journal.json")) == self.expected_journal,
                        "SEQUENCE_JOURNAL_DRIFT")
                require(c.inspect()["live_state_established"], "SEQUENCE_RUNTIME_DRIFT")
            else:
                p._cron(original=True)
            authorization = {"action": action, "context_sha256": d.sha(d.canonical(context)),
                "reference": "SEQ_" + d.sha(d.canonical({"sequence": self.reference, "action": action,
                    "ordinal": self.index, "nonce": uuid.uuid4().hex})),
                "operator": "UID1000_jazofv1", "expires_at": min(self.expires_at, p.ops.now() + 300),
                "exclusive_responsibility": True, "risks_acknowledged": list(RISKS)}
            require(getattr(p.ops, "_admission", None) is None, "NATIVE_OPERATION_ALREADY_ACTIVE")
            admission = _NativeAdmission(p.ops, self.coordinator, action, authorization)
            admission.monotonic_deadline = min(admission.monotonic_deadline, self.monotonic_deadline)
            p.ops._admission = admission
            try:
                result = self.coordinator.execute(action, authorization)
            finally:
                p.ops._admission = None  # Forget authority; NEVER perform recovery here.
            raw = c.fs.read(d.TX + "/journal.json"); value = c._journal()
            require(result.get("journal_sha256") == d.sha(d.canonical(value)), "SEQUENCE_RESULT_JOURNAL_DRIFT")
            expected = {"PREPARE": ("PREPARED", None), "PRESERVE": ("PREPARED", "PRESERVED"),
                "EXCLUDE": ("PREPARED", "EXCLUDED"), "ATTACH": ("PREPARED", "EXCLUDED"),
                "DRAIN": ("PREPARED", "DRAINED"), "ESTABLISH": ("PREPARED", "ESTABLISHED"),
                "COMMIT": ("COMMITTED", "INSTALLATION_VERIFIED"),
                "AUTHORIZE_RELEASE": ("COMMITTED", "RELEASE_AUTHORIZED"),
                "RESTORE_SCHEDULER": ("COMMITTED", "SCHEDULER_RESTORED"),
                "RELEASE": ("COMMITTED", "RELEASED")}[action]
            require((value["state"], value.get("window", {}).get("phase")) == expected and
                value["pending"] is None and c.inspect()["live_state_established"], "SEQUENCE_RESULT_UNCERTAIN")
            self.expected_journal = d.sha(raw)
            self.index += 1
            return action, result
        except BaseException:
            self.stopped = True
            raise  # No retry, rollback, cron restoration, release or adoption.


def _run_owner_approved_sequence(coordinator, resume=False):
    sequence = _ApprovedSequence(coordinator, resume=resume)
    print("Running the owner's approved fixed deployment process. No separate step approvals are requested.", flush=True)
    print("Keep exclusive responsibility: no independent/manual affected commands until verified release. Residual risks remain procedural; universal exclusion is not claimed.", flush=True)
    print(json.dumps({"sequence_authority": OWNER_SEQUENCE_AUTHORITY,
        "sequence_reference": sequence.reference, "resume": resume,
        "actions": list(sequence.actions), "manual_launch_control": "PROCEDURAL_ONLY"}, sort_keys=True), flush=True)
    for number in range(len(sequence.actions)):
        action, result = sequence.perform_next()
        print("Completed step " + str(number + 1) + " of " + str(len(sequence.actions)) + ": " + OPERATION_IMPACTS[action], flush=True)
        print(json.dumps({"result": "PASS_APPROVED_PROCESS_OPERATION", "action": action,
            "sequence_authority": OWNER_SEQUENCE_AUTHORITY, "sequence_reference": sequence.reference,
            "evidence": result, "pe7_executed": False, "universal_exclusion": False}, sort_keys=True), flush=True)
    print("Approved process completed and consumers explicitly released. PE-7.4 remains unauthorized.", flush=True)
    return 0


def run_deployment_sequence(coordinator):
    """Already owner-approved normal process; technical grants remain per operation."""
    return _run_owner_approved_sequence(coordinator)


def resume_native_main():
    """Only the precisely anchored PREPARED/EXCLUDED recovery approved on2026-10-27."""
    ops = NativeOps()
    fs = d.NativeFS()
    original = fs.read(BACKUP)
    lines = original.decode("utf-8", "strict").splitlines()
    inventory = {line: "EXCLUDE" if line in d.CRON else "PRESERVE"
        for line in lines if line.strip() and not line.lstrip().startswith("#")}
    require(len(inventory) == 12 and list(inventory.values()).count("EXCLUDE") == 3,
            "WINDOW_SCHEDULER_INVENTORY_CHANGED")
    coordinator = MaintenanceCoordinator.native(original, inventory)
    return _run_owner_approved_sequence(coordinator, resume=True)



if __name__ == "__main__":
    try:
        status = native_main()
    except BaseException as error:
        code = error.code if isinstance(error, d.Failure) else "NATIVE_OPERATION_STOPPED_UNCERTAIN"
        print(json.dumps({"result": "FAIL_STOP", "failure_code": code,
            "automatic_recovery": False, "consumer_release_implied": False,
            "pe7_executed": False, "STOP_REQUIRED": True}, sort_keys=True), flush=True)
        status = 1
    raise SystemExit(status)
