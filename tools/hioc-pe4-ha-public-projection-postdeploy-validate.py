"""Read-only source/baseline/installed review; never acquires process locks."""
import hashlib
import json
import re
import sys

SOURCE = "/home/jazofv1/hioc-release-source"
DEPLOY = "tools/hioc-pe4-ha-public-projection-deploy.py"
ENV = {"PATH":"/usr/bin:/bin","HOME":"/home/jazofv1","LANG":"C","LC_ALL":"C","GIT_OPTIONAL_LOCKS":"0"}

def review(ops, controller, mode, baseline=None):
    ops.source(ops.commit); ops.target()
    if mode == "BASELINE":
        result = ops.observe_baseline()
        raw = ops.cron_read(); controller.cron_candidate(raw,ops.expected_cron_sha)
        return result
    ops.installed_review(baseline)
    return None

def parse_args(args):
    if len(args) not in (4,6) or args[0]!="--preparation-commit" or args[2]!="--mode" or not re.fullmatch("[0-9a-f]{40}",args[1]): raise ValueError()
    if len(args)==4 and args[3]=="baseline":return args[1],"BASELINE",None
    if len(args)==6 and args[3]=="installed" and args[4]=="--baseline-sha256" and re.fullmatch("[0-9a-f]{64}",args[5]):return args[1],"INSTALLED",args[5]
    raise ValueError()

def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    out = {"RESULT":"FAIL","ERROR_CODE":"INVALID_ARGUMENT","MODE":None,"BASELINE":None,
           "BASELINE_REPORT_SHA256":None,"PUBLIC_PROJECTION_EXECUTION_EVIDENCE":"NOT_OBSERVED","STOP_REQUIRED":True,"PRODUCTION_MUTATED":False,"CRONTAB_MUTATED":False,
           "INVENTORY_LOCK_ACQUIRED":False,"ADAPTER_EXECUTED":False,"PUBLIC_PROJECTION_EXECUTED":False,
           "INVENTORY_ENGINE_EXECUTED":False,"MQTT_PUBLISHED":False,"HA_NETWORK_ATTEMPTED":False,"CREDENTIAL_ACCESSED":False}
    try:
        commit,mode,digest = parse_args(args)
        import os, pwd, socket, subprocess, types
        from pathlib import Path
        if sys.platform != "linux" or socket.gethostname() != "nutandpihole" or pwd.getpwuid(os.geteuid()).pw_name != "jazofv1" or Path(__file__).resolve() != Path(SOURCE)/"tools/hioc-pe4-ha-public-projection-postdeploy-validate.py": raise ValueError()
        # Read a bounded Git object with finite command timeout before importing
        # the trusted controller; no production operations exist in bootstrap.
        def git(path):
            size = subprocess.check_output(["/usr/bin/git","-c","core.fsmonitor=false","-C",SOURCE,"cat-file","-s",args[1]+":"+path],env=ENV,timeout=15,stderr=subprocess.DEVNULL)
            if not size.strip().isdigit() or int(size)>16*1024*1024: raise ValueError()
            raw = subprocess.check_output(["/usr/bin/git","-c","core.fsmonitor=false","-C",SOURCE,"show",args[1]+":"+path],env=ENV,timeout=15,stderr=subprocess.DEVNULL)
            if len(raw) > 16*1024*1024: raise ValueError()
            return raw
        raw = git(DEPLOY)
        if Path(SOURCE,DEPLOY).read_bytes() != raw or git("tools/hioc-pe4-ha-public-projection-postdeploy-validate.py") != Path(__file__).read_bytes(): raise ValueError()
        module = types.ModuleType("projection_deploy_review"); module.__file__ = str(Path(SOURCE,DEPLOY))
        exec(compile(raw,module.__file__,"exec"),module.__dict__)
        ops = module.NativeOps(args[1])
        out["MODE"] = args[3].upper()
        baseline = None
        if args[3] == "installed":
            receipt_fs = type(ops.fs)("/home/jazofv1",ops.uid,ops.gid)
            receipt_raw = receipt_fs.read("pe4-public-projection-baseline.json",0o600)
            module.require(receipt_raw is not None and module.sha(receipt_raw)==digest,"BASELINE_MISMATCH")
            receipt = module.strict_json(receipt_raw)
            out["BASELINE_REPORT_SHA256"] = digest
            module.require(receipt["RESULT"]=="PASS" and receipt["MODE"]=="BASELINE","BASELINE_REQUIRED")
            baseline = receipt["BASELINE"]
        out["BASELINE"] = review(ops,module,out["MODE"],baseline)
        out.update(RESULT="PASS",ERROR_CODE="NONE")
    except BaseException as exc:
        code = getattr(exc,"code",None)
        out["ERROR_CODE"] = code if code in {"SOURCE_BINDING","UNSAFE_OBJECT","BASELINE_REQUIRED","BASELINE_MISMATCH","CRONTAB_MISMATCH","CRONTAB_FAILED","TRANSACTION_CONFLICT","INSTALLED_MISMATCH","IO_FAILED"} else "INVALID_ARGUMENT"
    sys.stdout.write(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
    return 0 if out["RESULT"] == "PASS" else 1

if __name__ == "__main__": sys.exit(main())
