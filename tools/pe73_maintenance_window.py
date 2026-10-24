"""Bounded PE-7.3 maintenance-window provider. Native mutation is NOT qualified.

No CLI, automatic recovery, process killing, service control or universal exclusion.
The accepted Controller transaction methods and strict core journal validator are reused.
"""
import contextlib
import copy
import hashlib
import importlib.util
import os
import posixpath
from pathlib import Path
import re
import socket
import subprocess
import time
import uuid

PIN = "0589cf6363626d14ab9abe08c001ddef634b243326513b27de43a7b93aa4f95f"
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
    """Fixed read-only observations; mutating operations remain unconditionally gated."""
    def __init__(self):
        require(os.name == "posix" and socket.gethostname() == "nutandpihole" and
            os.getuid() == os.geteuid() == os.getgid() == os.getegid() == 1000, "TARGET_IDENTITY")
        self.boot_id = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        require(d.AUTH.fullmatch(self.boot_id), "BOOT_ID_UNAVAILABLE")
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
        raise d.Failure("NATIVE_WINDOW_ACCEPTANCE_REQUIRED")
    def scheduler_gate(self):
        # No receipt, boolean, CLI flag or environment variable unlocks this gate.
        raise d.Failure("NATIVE_SCHEDULER_NOT_QUALIFIED")
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
        self.ops.live_gate()  # Native mutation/coordination still unavailable pending native acceptance.
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
        return {"phase": w["phase"] if w else "NOT_ESTABLISHED", "journal_sha256": d.sha(d.canonical(value)),
            "scheduler_sha256": d.sha(self.ops.scheduler()), "process_observation": self.ops.processes(),
            "manual_launch_control": "PROCEDURAL_ONLY", "universal_exclusion": False,
            "native_qualified": False, "production_authorized": False}
