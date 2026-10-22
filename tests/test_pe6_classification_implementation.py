"""Separate immutable PE-6.0 acceptance and exact current PE-6.1 successor authority."""
import ast
import copy
import hashlib
import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE="ea4a93fba1615af1d6641c7f0683b8e912c03d72"
RECORD="governance/pe6/pe6-classification-implementation.json"
SCHEMA=RECORD.replace(".json",".schema.json")
DESIGN_RECORD="governance/pe6/pe6-classification-contract-design.json"
DESIGN_SCHEMA=DESIGN_RECORD.replace(".json",".schema.json")
DESIGN_DOCUMENT="docs/PE6_CLASSIFICATION_CONTRACT_DESIGN.md"
AUTHORIZED_PATHS=["ROADMAP.md","docs/CHANGELOG.md","docs/DATA_MODEL.md","docs/DEPLOYMENT.md","docs/HIOC_MASTER_PLAN.md","docs/HOME_ASSISTANT.md","docs/MQTT.md","docs/OPERATIONS.md","docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md","docs/PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md","docs/PE5_IMPLEMENTATION_PREPARATION.md","docs/PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md","docs/PE6_CLASSIFICATION_IMPLEMENTATION.md","docs/RELEASE.md","docs/SYSTEM_REFERENCE.md","governance/pe6/pe6-classification-implementation.json","governance/pe6/pe6-classification-implementation.schema.json","pi4/bin/hioc-classify-metadata.py","pi4/lib/hioc/classification.py","pi4/lib/hioc/classification_caller.py","pi4/lib/hioc/classification_contract.py","tests/test_pe4_documentation_consistency_correction.py","tests/test_pe4_ha_association_public_projection_test_binding_correction.py","tests/test_pe5_service_association_caller.py","tests/test_pe6_classification.py","tests/test_pe6_classification_contract_design.py","tests/test_pe6_classification_implementation.py"]

def git(*args):
    return subprocess.check_output(["git","--no-optional-locks",*args],cwd=ROOT,
        env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(path):return (ROOT/path).read_bytes().replace(b"\r\n",b"\n")
def sha(value):return hashlib.sha256(value).hexdigest()
def blob(value):return hashlib.sha1(b"blob "+str(len(value)).encode()+b"\0"+value).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()+b"\n"
def require(condition,reason):
    if not condition:raise ValueError(reason)
def closed(value):
    if type(value)is dict:return dict(type="object",additionalProperties=False,required=sorted(value),properties={k:closed(v) for k,v in sorted(value.items())})
    if type(value)is list:return dict(type="array",minItems=len(value),maxItems=len(value),prefixItems=[closed(v) for v in value],items=False)
    return dict(const=value)
def schema_for(value):
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-6.1 private classification repository implementation",**closed(value)}

@lru_cache(maxsize=None)
def historical(path):return git("show",BASE+":"+path)

def validate_historical_design(record,schema):
    """Original validator/path check, replayed only against exact accepted Git objects."""
    import test_pe6_classification_contract_design as prior
    original_git=prior.git
    def accepted_git(*args):
        if args==("diff","--name-only",prior.BASE):
            return original_git("diff","--name-only",prior.BASE,BASE)
        if args==("ls-files","--others","--exclude-standard"):
            return b""  # The immutable accepted commit has no untracked namespace.
        return original_git(*args)
    with patch.dict(prior.__dict__,raw=historical,git=accepted_git):
        return prior.validate_design(record,schema)

@lru_cache(maxsize=1)
def _accepted_design():
    # Cache only validation of immutable Git objects, never current file checks.
    record,schema=json.loads(historical(DESIGN_RECORD)),json.loads(historical(DESIGN_SCHEMA))
    require(historical(DESIGN_RECORD)==canonical(record) and historical(DESIGN_SCHEMA)==canonical(schema),"canonical historical design")
    return validate_historical_design(record,schema)

def accepted_design():
    require(all(raw(path)==historical(path) for path in [DESIGN_RECORD,DESIGN_SCHEMA,DESIGN_DOCUMENT]),"immutable PE6.0 design authority")
    return copy.deepcopy(_accepted_design())

def validate_implementation(record,schema,identities=True):
    require(schema==schema_for(record),"exact implementation schema")
    require(record["baseline_commit"]==BASE and record["checkpoint"]=="PE-6.1" and record["status"]=="IMPLEMENTED_REPOSITORY_ONLY","implementation authority")
    require(record["pe5_status"]=="COMPLETE/PASS" and record["pe6_0_status"]=="COMPLETE/PASS" and record["pe6_status"]=="IN_PROGRESS_REPOSITORY_IMPLEMENTED","phase boundaries")
    require(record["repository_implementation_authorized"] is True and record["production_authorized"] is False and all(record[k] is False for k in ["production_access","production_mutation","runtime_deployment_performed","runtime_execution_performed","pe6_2_started","public_projection_added","inventory_hook_added","scheduler_added","persistence_added"]),"implementation-only boundary")
    require(record["next_checkpoint"]=="PE-6.2 - PI3 Release-Source Synchronization" and record["full_native_suite_required"] is True,"next checkpoint and mandatory full suite")
    require(record["authorized_paths"]==AUTHORIZED_PATHS and {x["path"] for x in record["artifacts"]}|{RECORD,SCHEMA}==set(AUTHORIZED_PATHS),"finite implementation scope")
    design=accepted_design()
    require(record["design_adoption"]["commit"]==BASE and record["design_adoption"]["decision_ids"]==[x["id"] for x in design["decisions"]] and record["design_adoption"]["schema_sha256"]==sha(historical(DESIGN_SCHEMA)) and record["design_adoption"]["record_sha256"]==sha(historical(DESIGN_RECORD)),"exact adopted design")
    require([x["requirement"] for x in record["fixture_coverage"]]==design["required_implementation_fixtures"] and len(record["fixture_coverage"])==30,"complete adopted fixture ledger")
    require(all(x["evidence"] and x["disposition"] in ["REPOSITORY_SYNTHETIC_VALIDATION","DEFERRED_SEPARATE_NATIVE_CHECKPOINT"] for x in record["fixture_coverage"]),"fixture evidence not fabricated")
    if not identities:return record
    changed=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    require(changed==set(AUTHORIZED_PATHS),"unexpected implementation path")
    require(set(git("diff","--cached","--name-only",BASE).decode().splitlines())==set(AUTHORIZED_PATHS),"unexpected staged implementation path")
    entries=[row.split("\t",1) for row in git("ls-files","--stage").decode().splitlines()]
    require(all(row.split()[2]=="0" for row,path in entries),"unmerged implementation index")
    index={path:row.split()[:2] for row,path in entries}
    for item in record["artifacts"]:
        value=raw(item["path"])
        require((sha(value),blob(value))==(item["sha256"],item["git_blob"]),"current implementation artifact: "+item["path"])
        require(index.get(item["path"])==[item["mode"],blob(value)],"current staged artifact: "+item["path"])
    for path in [RECORD,SCHEMA]:
        require(index.get(path)==["100644",blob(raw(path))],"current staged governance: "+path)
    baseline=set(git("ls-tree","-r","--name-only",BASE).decode().splitlines())
    require({x["path"] for x in record["protected"]}==baseline-set(AUTHORIZED_PATHS),"complete protected baseline")
    for item in record["protected"]:
        value=historical(item["path"])
        require(raw(item["path"])==value and (sha(value),blob(value))==(item["sha256"],item["git_blob"]) and index.get(item["path"])==[item["mode"],item["git_blob"]],"protected baseline artifact: "+item["path"])
    from hioc.classification_contract import SCHEMA as output, RULES, DIMENSIONS
    require(output==design["proposed_output_schema"] and RULES==design["role_suggestion_contract"]["rules"] and DIMENSIONS==design["metadata_quality_contract"]["dimensions"],"adopted runtime constants")
    return record


# PE-6.2 owns only this explicit successor scope; PE-6.1 remains immutable authority.
ACCEPTED_IMPLEMENTATION="94f014cea1d5216a1deeef9fd1d0a025f1c7083e"
PE62_BASE="238dfae6cef1d4f17a4b1e52a5f636f01a5651c4"
PE62_PATHS=["docs/HIOC_MASTER_PLAN.md","docs/PE6_CLASSIFICATION_IMPLEMENTATION.md",
            "tests/test_pe6_classification_contract_design.py","tests/test_pe6_classification_implementation.py"]

@lru_cache(maxsize=None)
def accepted_bytes(path):
    return git("--no-replace-objects","show",ACCEPTED_IMPLEMENTATION+":"+path)

@lru_cache(maxsize=1)
def _accepted_index():
    rows=git("--no-replace-objects","ls-tree","-r","-z",ACCEPTED_IMPLEMENTATION).split(b"\0")
    return {path.decode():meta.decode().split()[::2] for row in rows if row for meta,path in [row.split(b"\t",1)]}

def accepted_index():return copy.deepcopy(_accepted_index())

def replay_implementation(record=None,schema=None):
    """Use the unchanged original PE-6.1 law with exact accepted Git inputs."""
    original_git=git
    def snapshot_git(*args):
        if args in [("diff","--name-only",BASE),("diff","--cached","--name-only",BASE)]:
            return original_git("--no-replace-objects","diff","--name-only",BASE,ACCEPTED_IMPLEMENTATION)
        if args==("ls-files","--others","--exclude-standard"):return b""
        if args==("ls-files","--stage"):
            return "".join(mode+" "+oid+" 0\t"+p+"\n" for p,(mode,oid) in sorted(accepted_index().items())).encode()
        return original_git(*args)
    r=json.loads(accepted_bytes(RECORD)) if record is None else record
    s=json.loads(accepted_bytes(SCHEMA)) if schema is None else schema
    require(accepted_bytes(RECORD)==canonical(json.loads(accepted_bytes(RECORD))) and
            accepted_bytes(SCHEMA)==canonical(json.loads(accepted_bytes(SCHEMA))),"canonical accepted implementation")
    with patch.dict(globals(),raw=accepted_bytes,git=snapshot_git):
        return validate_implementation(r,s)

@lru_cache(maxsize=1)
def _accepted_implementation():return replay_implementation()

def accepted_implementation():
    # Only immutable replay is cached; today's authority files are always checked.
    accepted_design()
    require(all(raw(p)==accepted_bytes(p) for p in [RECORD,SCHEMA]),"exact implementation schema / immutable PE6.1 evidence")
    return copy.deepcopy(_accepted_implementation())

def expected_master():
    text=accepted_bytes("docs/HIOC_MASTER_PLAN.md").decode()
    for heading in ["## Current Objective\n","## Next Planned Task\n"]:
        start=text.index(heading)+len(heading);end=text.index("### Historical",start)
        text=text[:start]+PE62_CURRENT+text[end:]
    text=text.replace("# Implementation Status\n","# Implementation Status\n\n"+PE62_STATUS,1)
    return text.encode()

def validate_pe62(record=None):
    old=accepted_implementation();index=accepted_index()
    require(git("rev-parse",PE62_BASE+"^{tree}")==git("rev-parse",ACCEPTED_IMPLEMENTATION+"^{tree}"),"accepted baseline tree")
    require(git("merge-base","--is-ancestor","4990c62afbce22a804229f3cb8329986741067a6",PE62_BASE)==b"","operator ancestry repository fact")
    require(git("branch","--show-current").decode().strip()=="main","current branch")
    head=git("rev-parse","HEAD").decode().strip()
    if head!=PE62_BASE:
        require(git("show","-s","--format=%P",head).decode().strip()==PE62_BASE,"current checkpoint parent")
        require(set(git("diff-tree","--no-commit-id","--name-only","-r",head).decode().splitlines())==set(PE62_PATHS),"committed successor scope")
        require(not git("diff","HEAD","--name-only"),"committed successor dirty")
    origin=git("rev-parse","origin/main").decode().strip()
    require(origin in [PE62_BASE,head] and git("rev-list","--left-right","--count","HEAD...origin/main").decode().split() in [["0","0"],["1","0"]],"current publication provenance")

    changed=set(git("diff","--name-only",PE62_BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    require(changed==set(PE62_PATHS),"unexpected implementation path / PE6.2 scope")
    require(set(git("diff","--cached","--name-only",PE62_BASE).decode().splitlines())==set(PE62_PATHS),"unexpected staged implementation path / PE6.2 scope")
    rows=[row.split("\t",1) for row in git("ls-files","--stage").decode().splitlines()]
    require(all(meta.split()[2]=="0" for meta,p in rows),"unmerged implementation index")
    current_index={p:meta.split()[:2] for meta,p in rows}
    require(set(current_index)==set(index),"unexpected index paths")
    for p,(mode,oid) in index.items():
        data=raw(p)
        if p not in PE62_PATHS:
            reason="current implementation artifact" if p in {i['path'] for i in old['artifacts']} else "protected baseline artifact"
            require(data==accepted_bytes(p) and blob(data)==oid,reason+": "+p)
        require(current_index.get(p)==[mode,blob(data)],"current staged artifact: "+p)
    require(raw("docs/HIOC_MASTER_PLAN.md")==expected_master(),"PE6.2 exact lifecycle / no false authorization")
    require(raw("docs/PE6_CLASSIFICATION_IMPLEMENTATION.md")==accepted_bytes("docs/PE6_CLASSIFICATION_IMPLEMENTATION.md")+PE62_REPORT.encode(),"PE6.2 exact operator evidence / historical prefix")
    # Each current artifact is provenance-checked above. Old authority objects are never rewritten.
    artifacts=[dict(item,sha256=sha(raw(item['path'])),git_blob=blob(raw(item['path']))) for item in old['artifacts']]
    value=dict(checkpoint="PE-6.2",status="COMPLETE/PASS",authorized_paths=list(PE62_PATHS),
               evidence_authority="OPERATOR_SUPPLIED",production_deployed=False,pe6_3_started=False,artifacts=artifacts)
    if record is not None:require(record==value,"exact current PE6.2 successor")
    return value

PE62_CURRENT='### PE-6.3 - Disabled Exact Runtime Deployment\n\nClassification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.\nPE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS_REPOSITORY_IMPLEMENTED.\nPE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS; PE6_2_STATUS=COMPLETE/PASS.\nPE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=FALSE.\nNEXT_CHECKPOINT=PE-6.3 - Disabled Exact Runtime Deployment.\nSeparate authorization is required for PE-6.3. PE6_3_STARTED=FALSE.\n\nPE-6.2 accepted source synchronization only from OPERATOR_SUPPLIED PI3 evidence:\nmain fast-forwarded to 238dfae6cef1d4f17a4b1e52a5f636f01a5651c4, clean, tree\nmatching accepted PE-6.1. Four PE-6 files were reported absent from runtime;\nsource and runtime directories were distinct. Codex did not observe PI3 directly.\nSee [PE-6.2 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-62-source-synchronization-acceptance-and-formal-closure).\nHistorical PE-6.0/PE-6.1 contracts and acceptance evidence remain unchanged.\nSource synchronization proves no production functionality, health, freshness or\nuniversal runtime-file preservation. No runtime deployment or caller execution occurred.\nPE-6.3 is disabled exact runtime deployment only, with no caller execution,\ninitialization, activation or cron; it is NOT STARTED and not authorized here.\nPE-6.4 remains later bounded execution and independent acceptance under separate authorization.\nNo recurring activation, automatic execution, PE-7 work or follow-on action is authorized.\n\n'
PE62_REPORT='\n\n## PE-6.2 source synchronization acceptance and formal closure\n\nClassification: CURRENT; repository closure candidate until required validation,\ncommit, push and independent publication verification pass.\nPE6_2_STATUS=COMPLETE/PASS; EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED.\nThis is source synchronization only, with no production functionality acceptance.\nAccepted PE-6.1 remains 94f014cea1d5216a1deeef9fd1d0a025f1c7083e.\nThe PE-6.0 design and PE-6.1 records/schemas and all preceding document bytes\nremain immutable historical evidence; their then-next PE-6.2 statements are historical.\n\n### Exact operator receipt and evidence limitations\n\nTarget: PI3 NUT&PIHOLE, hostname nutandpihole; all following PI3 facts are\nOPERATOR_SUPPLIED, not Codex observations or independently recomputed production hashes.\nSource: /home/jazofv1/hioc-release-source; runtime: /home/jazofv1/hioc.\nInitial source main, HEAD=origin/main=4990c62afbce22a804229f3cb8329986741067a6,\nclean working tree, no untracked files; remote=https://github.com/jorgeazofeifa-creator/hioc.git.\nFetch command git fetch --no-tags origin main returned 0; origin/main became\n238dfae6cef1d4f17a4b1e52a5f636f01a5651c4. Ancestor check returned 0.\ngit merge --ff-only origin/main returned 0. Final source HEAD=origin/main=\n238dfae6cef1d4f17a4b1e52a5f636f01a5651c4; final working tree clean.\nObserved source tree=aaf32cd1d0c9ce1dc1e6e00382322226030738d7,\nmatching accepted PE-6.1 tree. Local immutable Git history independently verifies\nancestry and tree equality; it does not independently observe PI3 state.\n\nAll four tracked source artifacts were observed ABSENT under the runtime root:\n- pi4/bin/hioc-classify-metadata.py\n- pi4/lib/hioc/classification.py\n- pi4/lib/hioc/classification_caller.py\n- pi4/lib/hioc/classification_contract.py\n\nObserved source directory inode=654548; runtime directory inode=802322;\nboth device=45826. They are distinct directories. No runtime deployment, caller\nexecution, scheduler activation, cron modification, service restart, MQTT operation\nor PI5 operation was performed during this checkpoint. These observations do not\nprove that every runtime file is unchanged, production health, current freshness,\ninput suitability, Linux execution semantics, or classification behavior in production.\nCodex accessed no PI3, PI5, Home Assistant, MQTT, credentials or production system.\nNo new observation time, transcript, staging-state field or runtime hash is invented.\n\n### Binding correction and validation boundary\n\nThe old current PE-6.1 validator froze exact current artifacts, path scope and next\ncheckpoint to PE-6.2. Its original validation body now replays the accepted PE-6.1\nGit snapshot with its exact original index, 27-path delta and protected identities.\nThe existing PE-6.0 historical replay remains independent. Fresh PE-6.2 validation\nowns exactly four paths: this document, HIOC_MASTER_PLAN.md and the two existing\nPE-6 design/implementation test modules. It does not inherit PE-6.1 edit authority.\nAll other accepted-tree artifacts, including all product/runtime sources and old\nrecords/schemas, remain byte/blob/mode-identical. Current stage-zero provenance,\nexact document changes, lifecycle, scope, historical evidence and unexpected paths\nare rechecked on every public current entry. Immutable Git bytes alone may be cached.\nPE-4/PE-5 consumers retain their existing delegation and original historical checks.\nTargeted historical/current, tamper, lifecycle, stage, cross-phase and protection\nregressions are required. The prior 2974-test suite remains PE-6.1 product acceptance;\nno runtime source changes occur here. Exact observed counts are recorded in the\nclosure commit/report, never substituted by historical totals. A failed gate blocks publication.\n\n### Next separate checkpoint\n\nPE6_1_STATUS=COMPLETE/PASS; PE6_REPOSITORY_IMPLEMENTED=TRUE;\nPE6_PRODUCTION_DEPLOYED=FALSE; PE6_3_STARTED=FALSE.\nNEXT_CHECKPOINT=PE-6.3 - Disabled Exact Runtime Deployment.\nSeparate authorization is required for PE-6.3: disabled exact runtime artifact\ninstallation only; no caller execution, initialization, activation or cron.\nPE-6.4 remains later separately authorized bounded execution and independent acceptance.\nNo recurring activation or automatic follow-on action is authorized. STOP after PE-6.2.\n\n### Preserved validation diagnosis\n\nThe initial focused correction run completed 50 tests: 49 passed, zero failures,\none error. A new substitution fixture called the patched raw reader recursively.\nIt now captures current bytes before historical replay patching; the unchanged\nhistorical validator must reject that substituted snapshot. This initial run is\nfailed evidence, not acceptance. Caller-visible scope/index values are copied to\nprevent mutation from changing later authority. Final observed validation totals\nare reported separately in the closure commit and Evidence Report.\n\nThe first complete affected run was 231 tests: 230 passed, zero failures, one error\nin the existing PE-5 status-section interface. The new current entry had required\nonly a full document, overlooking that established caller. It now accepts only\nthe exact freshly bound full document or its exact Implementation Status section;\nmodified or historical substitutes are still rejected. All PE-4/PE-5 test bodies\nremain unchanged. The complete focused and affected families are rerun after this\ncorrection; the failed attempt is preserved and is not acceptance evidence.\n'
PE62_STATUS='## PE-6.2 source synchronization closure\n\n### PE-6.3 - Disabled Exact Runtime Deployment\n\nClassification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.\nPE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS_REPOSITORY_IMPLEMENTED.\nPE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS; PE6_2_STATUS=COMPLETE/PASS.\nPE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=FALSE.\nNEXT_CHECKPOINT=PE-6.3 - Disabled Exact Runtime Deployment.\nSeparate authorization is required for PE-6.3. PE6_3_STARTED=FALSE.\n\nPE-6.2 accepted source synchronization only from OPERATOR_SUPPLIED PI3 evidence:\nmain fast-forwarded to 238dfae6cef1d4f17a4b1e52a5f636f01a5651c4, clean, tree\nmatching accepted PE-6.1. Four PE-6 files were reported absent from runtime;\nsource and runtime directories were distinct. Codex did not observe PI3 directly.\nSee [PE-6.2 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-62-source-synchronization-acceptance-and-formal-closure).\nHistorical PE-6.0/PE-6.1 contracts and acceptance evidence remain unchanged.\nSource synchronization proves no production functionality, health, freshness or\nuniversal runtime-file preservation. No runtime deployment or caller execution occurred.\nPE-6.3 is disabled exact runtime deployment only, with no caller execution,\ninitialization, activation or cron; it is NOT STARTED and not authorized here.\nPE-6.4 remains later bounded execution and independent acceptance under separate authorization.\nNo recurring activation, automatic execution, PE-7 work or follow-on action is authorized.\n\nAll earlier checkpoint narratives below retain their accepted historical meaning,\nincluding then-current labels and next-task snapshots. They do not supersede this\ncurrent status or Next Planned Task. PE-6.2 proves source synchronization only.\n\n'


# PE-6.2 remains a pinned historical checkpoint; PE-6.3 owns a smaller current scope.
ACCEPTED_PE62="723c1e71ad2d54e5088c0849ccee59857cbe0794"
PE63_BASE=ACCEPTED_PE62
PE63_PATHS=["docs/HIOC_MASTER_PLAN.md","docs/PE6_CLASSIFICATION_IMPLEMENTATION.md",
            "tests/test_pe6_classification_implementation.py"]

@lru_cache(maxsize=None)
def pe62_bytes(path):return git("--no-replace-objects","show",ACCEPTED_PE62+":"+path)

@lru_cache(maxsize=1)
def _pe62_index():
    rows=git("--no-replace-objects","ls-tree","-r","-z",ACCEPTED_PE62).split(b"\0")
    return {p.decode():m.decode().split()[::2] for row in rows if row for m,p in [row.split(b"\t",1)]}

def pe62_index():return copy.deepcopy(_pe62_index())

def replay_pe62(record=None):
    """Run the unchanged accepted PE-6.2 law and both original lifecycle interfaces."""
    original_git=git
    def snapshot_git(*args):
        if args in [("diff","--name-only",PE62_BASE),("diff","--cached","--name-only",PE62_BASE)]:
            return original_git("--no-replace-objects","diff","--name-only",PE62_BASE,ACCEPTED_PE62)
        if args in [("rev-parse","HEAD"),("rev-parse","origin/main")]:return (ACCEPTED_PE62+"\n").encode()
        if args==("branch","--show-current"):return b"main\n"
        if args==("rev-list","--left-right","--count","HEAD...origin/main"):return b"0\t0\n"
        if args in [("diff","HEAD","--name-only"),("ls-files","--others","--exclude-standard")]:return b""
        if args==("ls-files","--stage"):
            return "".join(mode+" "+oid+" 0\t"+p+"\n" for p,(mode,oid) in sorted(pe62_index().items())).encode()
        return original_git(*args)
    with patch.dict(globals(),raw=pe62_bytes,git=snapshot_git):
        value=validate_pe62(record)
        # Execute the actual accepted interface bodies, not approximated phrase tests.
        tree=ast.parse(pe62_bytes("tests/test_pe6_classification_implementation.py"))
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ["implementation_binding","assert_implementation_sequence"]]
        ns=dict(raw=pe62_bytes,sha=sha,blob=blob,require=require,PE62_CURRENT=PE62_CURRENT,implementation_successor=lambda:value)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),"<accepted PE6.2 interfaces>","exec"),ns)
        full=pe62_bytes("docs/HIOC_MASTER_PLAN.md").decode()
        status=full.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
        ns["assert_implementation_sequence"](full);ns["assert_implementation_sequence"](status)
        return value

@lru_cache(maxsize=1)
def _accepted_pe62():return replay_pe62()

def accepted_pe62():
    accepted_implementation()  # Fresh guards for unchanged PE-6.0/6.1 authority files.
    return copy.deepcopy(_accepted_pe62())

def expected_pe63_master():
    text=pe62_bytes("docs/HIOC_MASTER_PLAN.md").decode()
    for heading in ["## Current Objective\n","## Next Planned Task\n"]:
        start=text.index(heading)+len(heading);end=text.index("### Historical",start)
        text=text[:start]+PE63_CURRENT+text[end:]
    return text.replace("# Implementation Status\n","# Implementation Status\n\n"+PE63_STATUS,1).encode()

def validate_pe63(record=None):
    old=accepted_pe62();index=pe62_index()
    require(git("branch","--show-current").decode().strip()=="main","current branch")
    head=git("rev-parse","HEAD").decode().strip()
    if head!=PE63_BASE:
        require(git("show","-s","--format=%P",head).decode().strip()==PE63_BASE,"current checkpoint parent")
        require(set(git("diff-tree","--no-commit-id","--name-only","-r",head).decode().splitlines())==set(PE63_PATHS),"committed successor scope")
        require(not git("diff","HEAD","--name-only"),"committed successor dirty")
    require(git("rev-parse","origin/main").decode().strip() in [PE63_BASE,head] and
            git("rev-list","--left-right","--count","HEAD...origin/main").decode().split() in [["0","0"],["1","0"]],"current publication provenance")
    changed=set(git("diff","--name-only",PE63_BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    require(changed==set(PE63_PATHS),"unexpected implementation path / PE6.3 scope")
    require(set(git("diff","--cached","--name-only",PE63_BASE).decode().splitlines())==set(PE63_PATHS),"unexpected staged implementation path / PE6.3 scope")
    rows=[r.split("\t",1) for r in git("ls-files","--stage").decode().splitlines()]
    require(all(m.split()[2]=="0" for m,p in rows),"unmerged implementation index")
    staged={p:m.split()[:2] for m,p in rows};require(set(staged)==set(index),"unexpected index paths")
    for p,(mode,oid) in index.items():
        data=raw(p)
        if p not in PE63_PATHS:
            reason="current implementation artifact" if p in {i['path'] for i in old['artifacts']} else "protected baseline artifact"
            require(data==pe62_bytes(p) and blob(data)==oid,reason+": "+p)
        require(staged.get(p)==[mode,blob(data)],"current staged artifact: "+p)
    require(raw("docs/HIOC_MASTER_PLAN.md")==expected_pe63_master(),"PE6.3 exact lifecycle / no false execution authorization")
    require(raw("docs/PE6_CLASSIFICATION_IMPLEMENTATION.md")==pe62_bytes("docs/PE6_CLASSIFICATION_IMPLEMENTATION.md")+PE63_REPORT.encode(),"PE6.3 exact operator evidence / historical prefix")
    require(all(sha(raw(p))==h for p,h in PE63_INSTALLED.items()),"exact installed-source identity")
    require(sha(raw("pi4/lib/hioc/inventory.py"))=="4dad543d46c62a3335776d239f983082574361979200379990cf6c2ddfa3fb7e","preserved inventory source warning")
    artifacts=[dict(i,sha256=sha(raw(i['path'])),git_blob=blob(raw(i['path']))) for i in old['artifacts']]
    value=dict(checkpoint="PE-6.3",status="COMPLETE/PASS",authorized_paths=list(PE63_PATHS),
               artifacts=artifacts,evidence_authority="OPERATOR_SUPPLIED",production_deployed=True,
               deployment_scope="DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY",production_execution_established=False,
               scheduler_authorized=False,pe6_4_started=False)
    if record is not None:require(record==value,"exact current PE6.3 successor")
    return value

PE63_CURRENT='### PE-6.4 - Bounded Execution and Independent Production Acceptance\n\nClassification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.\nPE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.\nPE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;\nPE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.\nPE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.\nDEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.\nPE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.\nNEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.\nSeparate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.\n\nPE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from\nsource 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were\ninstalled without overwriting existing files; seven observed dependencies were preserved.\nCodex did not access PI3. No caller execution, initialization, cron change,\nservice restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.\nThe inspected activation locations returned no matches; universal indirect invocation\nabsence and current production health are not established.\nRuntime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and\nnormalize_mac AST definitions were reported equal. Full runtime compatibility is not established.\nRollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.\nSee [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).\nPE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.\nSTOP after PE-6.3. No automatic follow-on action is authorized.\n\n'
PE63_STATUS='## PE-6.3 disabled runtime installation closure\n\n### PE-6.4 - Bounded Execution and Independent Production Acceptance\n\nClassification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.\nPE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.\nPE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;\nPE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.\nPE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.\nDEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.\nPE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.\nNEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.\nSeparate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.\n\nPE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from\nsource 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were\ninstalled without overwriting existing files; seven observed dependencies were preserved.\nCodex did not access PI3. No caller execution, initialization, cron change,\nservice restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.\nThe inspected activation locations returned no matches; universal indirect invocation\nabsence and current production health are not established.\nRuntime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and\nnormalize_mac AST definitions were reported equal. Full runtime compatibility is not established.\nRollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.\nSee [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).\nPE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.\nSTOP after PE-6.3. No automatic follow-on action is authorized.\n\nAll earlier checkpoint narratives below retain their accepted historical meaning,\nincluding then-current labels and next-task snapshots. They do not supersede this\ncurrent status or Next Planned Task. Installation is not classification execution.\n\n'
PE63_REPORT="\n\n## PE-6.3 disabled runtime installation acceptance and closure\n\nPE6_3_STATUS=COMPLETE/PASS; EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED.\nAcceptance is disabled exact installation only, conditional on repository validation\nand publication gates. All preceding PE-6.1/PE-6.2 document bytes remain an exact\naccepted historical prefix; their deployment/next-task statements refer to those checkpoints.\nPE-6.0 design and PE-6.1 governance records/schemas are unchanged.\n\n### Source identity and operator-reported installation\n\nEvery PI3 statement below is OPERATOR_SUPPLIED, including the reported independent\npost-installation verification. Codex did not independently observe PI3.\nTarget: PI3 NUT&PIHOLE, hostname nutandpihole; Python 3.11.2.\nSource: /home/jazofv1/hioc-release-source; runtime: /home/jazofv1/hioc.\nSource main HEAD=origin/main=723c1e71ad2d54e5088c0849ccee59857cbe0794,\nclean; source and runtime directories separate. Source Git blobs were reported\nequal to working-file blobs. Each source file was regular, owner jazofv1:jazofv1,\nmode 644, one hard link. Local Git objects independently match the four supplied\nsource digests; this repository fact does not independently observe installed bytes.\nPREFLIGHT=PASS; INSTALLATION=PASS; POST_INSTALL_ARTIFACT_VERIFICATION=PASS.\nExactly four previously absent destination files were installed, with no overwrite.\n\n| Runtime-relative artifact | Accepted source / observed installed SHA-256 |\n|---|---|\n| pi4/bin/hioc-classify-metadata.py | 40d264d44ed9b52baa0abfc911afe98b29e84275e841769952922c66aafe5d03 |\n| pi4/lib/hioc/classification.py | 29b33e0ac6ad06b7b8eb360f10e9403ffb29993830eee16e21ff1b448bfd7f1c |\n| pi4/lib/hioc/classification_caller.py | b9238415e99d935b232481d8cb7a7f70adfbf2f353ed3e07f839810c540c78ca |\n| pi4/lib/hioc/classification_contract.py | 6be0c1cf21b159b74878ab1174e0239dd748f416d5c383ebd14091e45e533561 |\n\nAll four installed files were reported regular, one hard link, UID:GID 1000:1000,\nmode 0600. Destination parent directories already existed, were ordinary directories,\nowner jazofv1:jazofv1, mode 755. No additional installation or runtime copy is authorized here.\n\n### Seven existing dependencies preserved in the observed checks\n\nPROTECTED_DEPENDENCY_VERIFICATION=PASS. These before/after runtime identities\nwere supplied by the operator; they do not prove preservation of every runtime file.\nNo listed dependency was replaced or removed in this checkpoint.\n\n| Existing runtime dependency | Preserved operator-reported SHA-256 |\n|---|---|\n| assets.py | 9079c976e633d6d1f1c11bf051fc24ea5746500267f0fdfaf9ae1c5c8aea35c9 |\n| enrichment.py | ce3a60521bdb5b0d100e45d688b2a5847fbf56db1b87fce3ead0c65840d2804a |\n| manufacturer.py | 30d4ca1305b345442229395ac17b31a9e229ece08abc1f10732cb970c977cd08 |\n| service_association.py | dfdbab8bea085dfa0755e61b1952ee7991d663055c1f58b715997af751260bc5 |\n| configured_association.py | 9bab6fdfb0475a08d30c5d0c51c66ce3b9c841446047d420dccb41aa949357d8 |\n| configured_association_store.py | 1d5aa3d76a948e0f5bb0049f1abf8fd6cf2343be217796728ce66cee633c77b1 |\n| inventory.py | df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503 |\n\n### Explicit inventory.py discrepancy and compatibility limit\n\nAccepted source SHA-256:\n4dad543d46c62a3335776d239f983082574361979200379990cf6c2ddfa3fb7e\nExisting runtime SHA-256:\ndf1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503\nThe complete operator-observed diff has two differences: source imports\nfrom .core.compatibility import lease_observation; source adds\n_compatibility.pihole_leases to inventory output when hostname evidence is included.\nThe operator reported exactly equal AST definitions for KNOWN_FIELDS, OPERATOR_ROLES\nand normalize_mac. This establishes only those three definitions, not complete\nruntime compatibility, every dependency behavior, or successful caller execution.\nThe differing runtime inventory.py is intentionally preserved. No replacement or\ncompatibility repair is authorized by PE-6.3. This remains a production warning\nfor separately authorized PE-6.4 input/dependency acceptance.\n\n### Disabled activation: observed scope, not universal absence\n\nBefore installation, inspected locations returned no matching classification process,\nscheduler or runtime classification artifact. After installation, the operator inspected:\nuser crontab; /etc/crontab; /etc/cron.d; /etc/cron.hourly; /etc/cron.daily;\n/etc/cron.weekly; /etc/cron.monthly; /etc/systemd/system; /run/systemd/system;\nand running processes matching the classification entry point or caller.\nNo matching entries or processes were returned. Release-source working tree remained clean.\nNo universal absence of indirect invocation mechanisms is claimed. There is no\nclassification caller execution, initialization, cron modification, service restart,\nscheduled activation or PE-6.4 execution in this checkpoint's operator receipt.\nNo scheduler or automatic activation is authorized. Codex made no PI3/PI5,\nHome Assistant, MQTT, credential or production access or mutation.\n\n### Rollback boundary and remaining operational limitations\n\nROLLBACK=NOT_PERFORMED; ROLLBACK_TEST=NOT_ESTABLISHED.\nThe provenance-bound prior state is absence of precisely the four installed files;\nno pre-existing destination bytes were overwritten or require backup restoration.\nNo backup/archive location or completed rollback receipt was supplied or is invented.\nA future rollback requires separate operator authorization. First verify the exact\nfour destination paths, installed SHA-256 values, regular-file/owner/mode/link identities,\nand relevant runtime-use conditions; resolve any change or use uncertainty before removal.\nIf all authorized preconditions hold, remove only those four specifically installed\nartifacts to restore their prior absence. Preserve every pre-existing dependency,\nparent directory, operator input, existing runtime configuration and historical journal.\nStop on identity drift or unresolved use; do not replace/delete inventory.py or perform\nunrelated cleanup. Recheck the four-file absence and protected dependencies afterward.\nThis documents the bounded procedure; it is not an executed or fully tested rollback,\na production command authorization, or a universal proof of disabled invocation.\n\n### Repository acceptance and next separate gate\n\nHistorical PE-6.1 validates at 94f014cea1d5216a1deeef9fd1d0a025f1c7083e.\nHistorical PE-6.2 validates its unchanged original four-path law and full/status\ninterfaces at 723c1e71ad2d54e5088c0849ccee59857cbe0794. Fresh current PE-6.3\nowns only this document, HIOC_MASTER_PLAN.md and the implementation-binding test\nmodule. All other accepted-tree files, product sources and old records/schemas\nremain byte/blob/mode-identical. Full-document and exact Implementation Status\ninterfaces are retained; historical/current substitution and altered receipts are rejected.\nOnly immutable Git data/replay may be cached; current scope, stage, artifacts,\nclosed evidence, lifecycle and protected files are checked afresh.\nFast static/negative, focused PE-6 and directly affected PE-4/PE-5 tests precede\npublication. Exact observed totals belong to the closure commit and Evidence Report.\nThe accepted 2974-test PE-6.1 product suite is historical evidence, not a new test run;\nno product implementation changes occur here. Failed gates prevent publication.\nPE-6 remains IN PROGRESS; PE-6.3 COMPLETE/PASS is disabled installation only.\nPE-6.4 bounded execution and independent acceptance is NEXT / NOT STARTED and\nrequires separate authorization. No caller execution, activation or follow-on action\nis authorized by this closure. STOP after PE-6.3.\n"
PE63_INSTALLED={'pi4/bin/hioc-classify-metadata.py': '40d264d44ed9b52baa0abfc911afe98b29e84275e841769952922c66aafe5d03', 'pi4/lib/hioc/classification.py': '29b33e0ac6ad06b7b8eb360f10e9403ffb29993830eee16e21ff1b448bfd7f1c', 'pi4/lib/hioc/classification_caller.py': 'b9238415e99d935b232481d8cb7a7f70adfbf2f353ed3e07f839810c540c78ca', 'pi4/lib/hioc/classification_contract.py': '6be0c1cf21b159b74878ab1174e0239dd748f416d5c383ebd14091e45e533561'}

# Historical PE-6.3 is immutable; the timestamp prerequisite has its own finite scope.
CORRECTION_BASE='b83f56d19912b2b36b689cf95af8a56a45d02474'
CORRECTION_PATHS=['docs/HIOC_MASTER_PLAN.md', 'docs/PE6_CLASSIFICATION_IMPLEMENTATION.md', 'pi4/lib/hioc/classification.py', 'tests/test_pe6_classification.py', 'tests/test_pe6_classification_implementation.py']
CORRECTION_CURRENT='### PE-6.4 - Bounded Execution and Independent Production Acceptance\n\nClassification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.\nPE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.\nPE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;\nPE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.\nPE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.\nDEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.\nPE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.\nNEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.\nSeparate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.\n\nPE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from\nsource 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were\ninstalled without overwriting existing files; seven observed dependencies were preserved.\nCodex did not access PI3. No caller execution, initialization, cron change,\nservice restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.\nThe inspected activation locations returned no matches; universal indirect invocation\nabsence and current production health are not established.\nRuntime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and\nnormalize_mac AST definitions were reported equal. Full runtime compatibility is not established.\nRollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.\nSee [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).\nPE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.\n### Timestamp compatibility correction prerequisite\n\nTIMESTAMP_CORRECTION=REPOSITORY_ONLY; CORRECTED_ARTIFACT_DEPLOYED=NOT_ESTABLISHED.\nPE6_4_STARTED=FALSE; PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE.\nThe operator reported inventory.updated=2026-10-17T11:00:02-06:00,\n198 parseable devices and freshness at inspection only (OPERATOR_SUPPLIED).\nThe PE-6.3 installed classifier rejects that accepted PE-5 aware-time form.\nThe repository correction accepts aware offsets and emits UTC without rewriting inputs.\nProduction still requires separate operator source synchronization, guarded replacement\nof classification.py only, then separately authorized bounded PE-6.4 execution.\nNo deployment, caller execution, scheduling, PE-6.4 closure or PE-7 is authorized here.\nSee [Timestamp correction evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md#timestamp-compatibility-correction-prerequisite-to-pe-64).\n\nSTOP after the repository correction. No automatic follow-on action is authorized.\n\n'
CORRECTION_STATUS='## Timestamp compatibility repository correction (PE-6.4 prerequisite)\n\n### PE-6.4 - Bounded Execution and Independent Production Acceptance\n\nClassification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.\nPE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.\nPE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;\nPE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.\nPE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.\nDEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.\nPE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.\nNEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.\nSeparate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.\n\nPE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from\nsource 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were\ninstalled without overwriting existing files; seven observed dependencies were preserved.\nCodex did not access PI3. No caller execution, initialization, cron change,\nservice restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.\nThe inspected activation locations returned no matches; universal indirect invocation\nabsence and current production health are not established.\nRuntime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and\nnormalize_mac AST definitions were reported equal. Full runtime compatibility is not established.\nRollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.\nSee [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).\nPE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.\n### Timestamp compatibility correction prerequisite\n\nTIMESTAMP_CORRECTION=REPOSITORY_ONLY; CORRECTED_ARTIFACT_DEPLOYED=NOT_ESTABLISHED.\nPE6_4_STARTED=FALSE; PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE.\nThe operator reported inventory.updated=2026-10-17T11:00:02-06:00,\n198 parseable devices and freshness at inspection only (OPERATOR_SUPPLIED).\nThe PE-6.3 installed classifier rejects that accepted PE-5 aware-time form.\nThe repository correction accepts aware offsets and emits UTC without rewriting inputs.\nProduction still requires separate operator source synchronization, guarded replacement\nof classification.py only, then separately authorized bounded PE-6.4 execution.\nNo deployment, caller execution, scheduling, PE-6.4 closure or PE-7 is authorized here.\nSee [Timestamp correction evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md#timestamp-compatibility-correction-prerequisite-to-pe-64).\n\nSTOP after the repository correction. No automatic follow-on action is authorized.\n\nEarlier checkpoint entries below remain historical evidence.\n\n'
CORRECTION_REPORT="\n\n## Timestamp compatibility correction prerequisite to PE-6.4\n\nREPOSITORY_TIMESTAMP_CORRECTION=PREPARED_FOR_VALIDATION_AND_PUBLICATION.\nThis section records a repository correction, not PE-6.4 production acceptance.\nAll preceding PE-6.1/6.2/6.3 Evidence Report bytes are preserved exactly from\nb83f56d19912b2b36b689cf95af8a56a45d02474. Their installation identities describe\nthat historical receipt, not deployment of the corrected classifier.\n\n### Cause, timestamp dependency analysis and exact correction\n\nOPERATOR_SUPPLIED: inventory.updated was 2026-10-17T11:00:02-06:00;\nJSON parseable, 198 devices, fresh at inspection; classification not executed.\nThese are supplied observations, not Codex production access or current freshness.\nThe PE-5 service_association.TIMESTAMP_PATTERN/_time parser already accepts aware\nZ and +/-HH:MM timestamps and normalizes to UTC. PE-6 timestamp() imposed an\nadditional Z-only gate before delegating to it, rejecting valid offset inventory.\nThe classifier now uses that accepted grammar/parser, with explicit offset-hour\nand minute bounds to reject fromisoformat's normalization of malformed +01:60.\nNaive timestamps, unsupported forms, invalid dates and impossible times fail closed\nwith the existing CLOCK_INVALID safe code. No input or inventory file is rewritten.\n\nAll timestamp() consumers were traced: evaluation clock; inventory.updated and\nits 2100-second deadline; hostname candidate observed_at comparison; PE-5 handoff\nvalid_until cap; result original/current time, deadline and backwards-clock checks.\nExternal inventory and paired hostname/manufacturer generated_at remain unchanged\nin captured source bytes and SHA-256 provenance. UTC projection is used only in\noutput proof timestamps. Caller-generated clocks and deadline output remain UTC.\nOffset evaluation values are projected to canonical UTC; existing Z representation\nis retained. The immutable closed PE-6 output schema, rules and dimensions are\nunchanged. _hostname retains exact generated_at/inventory.updated source pairing;\nequivalent time does not substitute for exact source identity. _handoff continues\nusing PE-5's original confirmation, schema, inventory-digest and expiry authority.\nNo source-specific validator is weakened. Result validation rederives from current\ninputs, rechecks original fingerprints and temporal validity, and rejects reencoding\nof a bound source even when it denotes the same instant. Caller Reader/fingerprint,\nrecheck/lock code and CLI remain byte-identical. Missing/rejected required inventory\nremains UNAVAILABLE with no fabricated devices. Future times, backwards clocks and\nrejection exactly at 2100 seconds remain protected. Identity, canonical IP, health,\nliveness, public inventory, MQTT and every other runtime source remain unchanged.\n\n### Regression and historical authority\n\nDeterministic fixtures cover Z, -06:00, positive offsets, equal instants, fresh\noffset inventory, raw identity, UTC output schema, exclusive 2100-second deadline,\nfuture/backwards time, naive/malformed offsets, calendar/time errors, exact hostname\npairing and confirmed PE-5 handoff. Existing privacy/provenance/caller tests remain.\nThe accepted design requires a full native suite for product source changes.\nFocused timestamp, PE-6 contract/caller, affected cross-phase and full native tests\nmust all pass before publication; exact observed totals are retained in the commit\nand Evidence Report. Environment skips are not passes or Linux production proof.\n\nPE-6.1/6.2/6.3 original validators and authoritative constants remain unchanged.\nHistorical PE-6.3 replays its exact accepted Git bytes, original three-path scope,\ninstalled-source hashes and full/status interfaces. The fresh current correction\nowns exactly five paths: classification.py, its existing product test, the existing\nimplementation-binding test and these two documents. Existing PE-4/PE-5 consumers\ncontinue delegating to the current successor map. Every other accepted artifact,\nold governance record/schema and executable remains byte/blob/mode-identical.\nNew current validation checks scope/index/modes, exact correction source/test\nidentities, document changes, protected files and publication lineage afresh.\nOnly immutable Git snapshots/replays are cached. New negatives protect historical\nidentity/authority against current substitution and false production acceptance.\n\n### Required next operator-only action and retained limitations\n\nNo PI3/PI5, HA, MQTT, credential or production access/mutation occurred. The accepted\nPE-6.3 installed classification.py SHA-256 remains historically\n29b33e0ac6ad06b7b8eb360f10e9403ffb29993830eee16e21ff1b448bfd7f1c.\nIt does not prove current runtime bytes. Corrected artifact deployment and production\nexecution are NOT ESTABLISHED. PE-6.4 is NOT CLOSED; PE-6 remains IN_PROGRESS.\nThe previously reported runtime/source inventory.py difference and limited three-AST\ncomparison remain unresolved full-compatibility warnings. No inventory replacement,\nthreshold change, scheduled activation or automatic follow-on is authorized.\n\nNext requires separate operator authorization: fast-forward the clean PI3 release\nsource checkout to the published correction commit, verify its exact tree and\nclassification.py Git blob/SHA-256, and prepare a guarded one-file replacement of\n/home/jazofv1/hioc/pi4/lib/hioc/classification.py from that source. First establish\ncurrent runtime-use conditions and match the historical installed classifier hash,\nordinary path/parent identities, UID:GID 1000:1000, mode 0600 and single link; stop\non drift or unresolved use. Preserve exact old bytes and metadata as a private,\nnon-overwriting rollback backup, then replace only this artifact atomically with\nverified corrected bytes, preserving ownership/mode and rechecking destination\nhash/identity and all other PE-6 artifacts/dependencies. Do not execute classification,\nchange inventory, scheduling or services. Deployment receipt must be accepted before\nseparately authorized bounded PE-6.4 execution. This describes the next gate; it is\nnot an operator deployment command or authorization to perform it now. STOP.\n"
CORRECTION_IDENTITIES={'pi4/lib/hioc/classification.py': 'feda2fc41c374d84728e1601b616875cda8289f489fbd903c107409a8fa5a2f6', 'tests/test_pe6_classification.py': '197dd50176c3610c21c040ec8bc7aa66832fd389ef4d67c3a916f6f522f85c82'}

@lru_cache(maxsize=None)
def pe63_bytes(path):return git("--no-replace-objects","show",CORRECTION_BASE+":"+path)

@lru_cache(maxsize=1)
def _pe63_index():
    rows=git("--no-replace-objects","ls-tree","-r","-z",CORRECTION_BASE).split(b"\0")
    return {p.decode():m.decode().split()[::2] for row in rows if row for m,p in [row.split(b"\t",1)]}

def pe63_index():return copy.deepcopy(_pe63_index())

def replay_pe63(record=None):
    original_git=git
    def snapshot_git(*args):
        if args in [("diff","--name-only",PE63_BASE),("diff","--cached","--name-only",PE63_BASE)]:
            return original_git("--no-replace-objects","diff","--name-only",PE63_BASE,CORRECTION_BASE)
        if args in [("rev-parse","HEAD"),("rev-parse","origin/main")]:return (CORRECTION_BASE+"\n").encode()
        if args==("branch","--show-current"):return b"main\n"
        if args==("rev-list","--left-right","--count","HEAD...origin/main"):return b"0\t0\n"
        if args in [("diff","HEAD","--name-only"),("ls-files","--others","--exclude-standard")]:return b""
        if args==("ls-files","--stage"):
            return "".join(mode+" "+oid+" 0\t"+p+"\n" for p,(mode,oid) in sorted(pe63_index().items())).encode()
        return original_git(*args)
    with patch.dict(globals(),raw=pe63_bytes,git=snapshot_git):
        value=validate_pe63(record)
        tree=ast.parse(pe63_bytes("tests/test_pe6_classification_implementation.py"))
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ["implementation_binding","assert_implementation_sequence"]]
        ns=dict(raw=pe63_bytes,sha=sha,blob=blob,require=require,PE63_CURRENT=PE63_CURRENT,implementation_successor=lambda:value)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),"<accepted PE6.3 interfaces>","exec"),ns)
        full=pe63_bytes("docs/HIOC_MASTER_PLAN.md").decode()
        status=full.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
        ns["assert_implementation_sequence"](full);ns["assert_implementation_sequence"](status)
        return value

@lru_cache(maxsize=1)
def _accepted_pe63():return replay_pe63()

def accepted_pe63():
    accepted_pe62()
    return copy.deepcopy(_accepted_pe63())

def expected_correction_master():
    text=pe63_bytes("docs/HIOC_MASTER_PLAN.md").decode()
    for heading in ["## Current Objective\n","## Next Planned Task\n"]:
        start=text.index(heading)+len(heading);end=text.index("### Historical",start)
        text=text[:start]+CORRECTION_CURRENT+text[end:]
    return text.replace("# Implementation Status\n","# Implementation Status\n\n"+CORRECTION_STATUS,1).encode()

def validate_timestamp_correction(record=None):
    old=accepted_pe63();index=pe63_index()
    require(git("branch","--show-current").decode().strip()=="main","current branch")
    head=git("rev-parse","HEAD").decode().strip()
    if head!=CORRECTION_BASE:
        require(git("show","-s","--format=%P",head).decode().strip()==CORRECTION_BASE,"current checkpoint parent")
        require(set(git("diff-tree","--no-commit-id","--name-only","-r",head).decode().splitlines())==set(CORRECTION_PATHS),"committed successor scope")
        require(not git("diff","HEAD","--name-only"),"committed successor dirty")
    require(git("rev-parse","origin/main").decode().strip() in [CORRECTION_BASE,head] and
            git("rev-list","--left-right","--count","HEAD...origin/main").decode().split() in [["0","0"],["1","0"]],"current publication provenance")
    changed=set(git("diff","--name-only",CORRECTION_BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    require(changed==set(CORRECTION_PATHS),"unexpected implementation path / PE6.3 scope")
    require(set(git("diff","--cached","--name-only",CORRECTION_BASE).decode().splitlines())==set(CORRECTION_PATHS),"unexpected staged implementation path / PE6.3 scope")
    rows=[r.split("\t",1) for r in git("ls-files","--stage").decode().splitlines()]
    require(all(m.split()[2]=="0" for m,p in rows),"unmerged implementation index")
    staged={p:m.split()[:2] for m,p in rows};require(set(staged)==set(index),"unexpected index paths")
    for p,(mode,oid) in index.items():
        data=raw(p)
        if p not in CORRECTION_PATHS:
            reason="current implementation artifact" if p in {i['path'] for i in old['artifacts']} else "protected baseline artifact"
            require(data==pe63_bytes(p) and blob(data)==oid,reason+": "+p)
        require(staged.get(p)==[mode,blob(data)],"current staged artifact: "+p)
    require(raw("docs/HIOC_MASTER_PLAN.md")==expected_correction_master(),"PE6.3 exact lifecycle / no false execution authorization")
    require(raw("docs/PE6_CLASSIFICATION_IMPLEMENTATION.md")==pe63_bytes("docs/PE6_CLASSIFICATION_IMPLEMENTATION.md")+CORRECTION_REPORT.encode(),"PE6.3 exact operator evidence / historical prefix")
    require(all(sha(raw(p))==h for p,h in CORRECTION_IDENTITIES.items()),"exact corrected source/test identity")
    require(sha(raw("pi4/lib/hioc/inventory.py"))=="4dad543d46c62a3335776d239f983082574361979200379990cf6c2ddfa3fb7e","preserved inventory source warning")
    artifacts=[dict(i,sha256=sha(raw(i['path'])),git_blob=blob(raw(i['path']))) for i in old['artifacts']]
    value=dict(checkpoint="PE-6.4_TIMESTAMP_COMPATIBILITY_CORRECTION",status="REPOSITORY_CORRECTION_ONLY",authorized_paths=list(CORRECTION_PATHS),
               artifacts=artifacts,evidence_authority="OPERATOR_SUPPLIED",production_deployed=True,
               deployment_scope="DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY",production_execution_established=False,
               scheduler_authorized=False,pe6_4_started=False,corrected_artifact_deployment_established=False)
    if record is not None:require(record==value,"exact current PE6.3 successor")
    return value


def implementation_successor():
    if not globals().get('_PE7_HISTORICAL_REPLAY', False):
        from test_pe7_binding import current_candidate
        candidate=current_candidate(read=raw, git_runner=git)
        # Read-only inherited bindings preserve the established consumer map;
        # they do not grant edit authority over the protected baseline.
        inherited={item['path'] for item in accepted_implementation()['artifacts']}
        merged={item['path']:item for item in candidate['protected'] if item['path'] in inherited}
        merged.update({item['path']:item for item in candidate['artifacts']})
        return dict(candidate, artifacts=[merged[path] for path in sorted(merged)])
    return validate_timestamp_correction()

def historical_implementation_candidate():
    record,schema=json.loads(raw(RECORD)),json.loads(raw(SCHEMA))
    require(raw(RECORD)==canonical(record) and raw(SCHEMA)==canonical(schema),"canonical implementation")
    return validate_implementation(record,schema)

def implementation_binding(path):
    successor=implementation_successor()
    item=next((x for x in successor["artifacts"] if x["path"]==path),None)
    if item:
        value=raw(path)
        require(sha(value)==item['sha256'] and (blob(value)==item['git_blob'] or
            value==git('cat-file','blob',item['git_blob']).replace(b'\r\n',b'\n')),'current successor identity')
    return item

def assert_implementation_sequence(text):
    if not globals().get('_PE7_HISTORICAL_REPLAY', False):
        from test_pe7_binding import assert_candidate_sequence
        return assert_candidate_sequence(text, read=raw, git_runner=git)
    implementation_binding("docs/HIOC_MASTER_PLAN.md")
    full=raw("docs/HIOC_MASTER_PLAN.md").decode()
    status=full.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
    require(text in (full,status),"current lifecycle text substitution")
    section=full.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(section=="\n"+CORRECTION_CURRENT,"current PE6.3 successor / PE6.4 separate authorization")


@lru_cache(maxsize=4096)
def _immutable_replay_command(repository_root, args):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=repository_root,
        env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'), stderr=subprocess.PIPE)

def load_tests(loader, tests, pattern, *, namespaces=()):
    """Replay these historical governance fixtures at their immutable accepted commit.

    Current PE-7 bindings have separate negative fixtures in test_pe7_binding.
    No historical function/class body, record, schema or identity is refreshed.
    The synthetic index below describes a Git COMMIT, never the current index.
    """
    import io
    import tempfile
    import zipfile
    from contextlib import ExitStack
    accepted = '9d6ce274a80a578d488d7245ebfa5bca1d5f5a83'
    repository_root = ROOT
    namespace_git = {id(namespace): namespace['git'] for namespace in namespaces
        if 'git' in namespace and namespace.get('_pe7_original_git', namespace['git']) is not namespace['git']}
    @lru_cache(maxsize=None)
    def repository_git(*args):
        # Only explicitly immutable object/ref arguments enter the shared cache.
        # HEAD/index/current-tree observations are never cached across replays.
        if any(__import__('re').match(r'^[0-9a-f]{40}(?::|\^|$)', arg) for arg in args) and not any(
                'HEAD' in arg or 'origin/' in arg or arg.startswith(':') for arg in args):
            return _immutable_replay_command(repository_root, args)
        return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=repository_root,
            env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'), stderr=subprocess.PIPE)
    class HistoricalSuite(unittest.TestSuite):
        def run(self, result, debug=False):
            with tempfile.TemporaryDirectory(prefix='hioc-pe6-historical-') as directory:
                snapshot = Path(directory)
                archive = zipfile.ZipFile(io.BytesIO(repository_git('archive', '--format=zip', accepted)))
                for member in archive.infolist():
                    path = __import__('pathlib').PurePosixPath(member.filename)
                    require(not path.is_absolute() and '..' not in path.parts, 'historical archive path')
                    require((member.external_attr >> 16) & 0o170000 != 0o120000, 'historical archive link')
                archive.extractall(snapshot)
                # This selected historical law hashes two unnormalized source
                # files. Reproduce their recorded Git representation, never a
                # guessed LF conversion or a refreshed historical identity.
                if any(namespace.get('__name__', '').endswith('test_pe4_ha_runtime_credential_provisioning_closure') for namespace in namespaces):
                    correction = json.loads(repository_git('--no-replace-objects', 'show', accepted+':governance/pe4/pe4-ha-association-runtime-validation-correction.json'))
                    for path in ('pi4/lib/hioc/home_assistant_association.py', 'pi4/bin/hioc-home-assistant-association.py'):
                        binding = next(item for item in correction['sources'].values() if item['path'] == path)
                        content = repository_git('--no-replace-objects', 'show', accepted+':'+path)
                        require((sha(content), blob(content)) == (binding['sha256'], binding['git_blob']), 'historical raw source identity')
                        (snapshot/path).write_bytes(content)
                git_directory = repository_git('rev-parse', '--absolute-git-dir').decode().strip()
                (snapshot/'.git').write_text('gitdir: '+git_directory+'\n', encoding='utf-8')
                def historical_git(*args):
                    if args == ('branch', '--show-current'): return b'main\n'
                    if args in [('rev-parse', 'HEAD'), ('rev-parse', 'origin/main')]: return (accepted+'\n').encode()
                    if args == ('rev-list', '--left-right', '--count', 'HEAD...origin/main'): return b'0\t0\n'
                    if args == ('ls-files', '--others', '--exclude-standard'): return b''
                    if args == ('ls-files', '--stage'):
                        rows = repository_git('ls-tree', '-r', accepted).decode().splitlines()
                        return ''.join(f'{meta.split()[0]} {meta.split()[2]} 0\t{path}\n'
                                       for meta,path in (row.split('\t',1) for row in rows)).encode()
                    if args == ('diff', 'HEAD', '--name-only'): return b''
                    if args[:1] == ('diff',):
                        split = args.index('--') if '--' in args else len(args)
                        positional = [arg for arg in args[1:split] if not arg.startswith('-')]
                        if len(positional) == 1:
                            return repository_git(*[arg for arg in args[:split] if arg != '--cached'], accepted, *args[split:])
                        if not positional: return b''
                    return repository_git(*(accepted if arg in ('HEAD', 'origin/main') else accepted+arg
                        if arg.startswith(':') else arg for arg in args))
                import test_pe5_service_association_caller as caller
                snapshot_read = lambda path:(snapshot/path).read_bytes().replace(b'\r\n',b'\n')
                class OriginalCandidateSuite(unittest.TestSuite):
                    def run(self, result, debug=False):
                        nonlocal accepted
                        later = accepted
                        accepted = ACCEPTED_IMPLEMENTATION
                        try:
                            with tempfile.TemporaryDirectory(prefix='hioc-pe61-candidate-') as original_directory:
                                original_root = Path(original_directory)
                                original_archive = zipfile.ZipFile(io.BytesIO(repository_git('archive', '--format=zip', accepted)))
                                for member in original_archive.infolist():
                                    candidate_path = __import__('pathlib').PurePosixPath(member.filename)
                                    require(not candidate_path.is_absolute() and '..' not in candidate_path.parts, 'historical archive path')
                                    require((member.external_attr >> 16) & 0o170000 != 0o120000, 'historical archive link')
                                original_archive.extractall(original_root)
                                # The accepted record distinguishes canonical Git
                                # bytes from its original Windows checkout bytes.
                                # Reproduce only an encoding whose exact recorded
                                # identity is independently verified; no new hash.
                                original_record = json.loads((original_root/RECORD).read_bytes())
                                for item in original_record['preserved_candidate_unmodified']:
                                    fixture = original_root/item['path']
                                    git_bytes = repository_git('--no-replace-objects', 'show', accepted+':'+item['path'])
                                    require(sha(git_bytes) == item['sha256'] == item['file_sha256'],
                                            'historical candidate bytes unavailable')
                                    fixture.write_bytes(git_bytes)
                                original_read = lambda path:(original_root/path).read_bytes().replace(b'\r\n',b'\n')
                                with patch.dict(caller.__dict__, ROOT=original_root, raw=original_read), patch.dict(globals(), ROOT=original_root, raw=original_read):
                                    return super().run(result, debug)
                        finally:
                            accepted = later
                def bind_original_candidate(suite):
                    children = []
                    for test in suite:
                        if isinstance(test, unittest.TestSuite):
                            children.append(bind_original_candidate(test))
                        elif test._testMethodName == 'test_original_five_file_candidate_and_asset_correction_retained':
                            # This assertion owns the PE-6.1 candidate, not the later
                            # explicitly authorized timestamp source correction.
                            children.append(OriginalCandidateSuite([test]))
                        else:
                            children.append(test)
                    return unittest.TestSuite(children)
                bound_tests = bind_original_candidate(tests)
                with ExitStack() as stack:
                    stack.enter_context(patch.dict(os.environ, GIT_OPTIONAL_LOCKS='0',
                        GIT_DIR=git_directory, GIT_WORK_TREE=str(snapshot)))
                    stack.enter_context(patch.dict(caller.__dict__, ROOT=snapshot, git=historical_git, raw=snapshot_read))
                    stack.enter_context(patch.dict(globals(), ROOT=snapshot, git=historical_git,
                                                   raw=snapshot_read, _PE7_HISTORICAL_REPLAY=True))
                    # A historical dependency graph must read one historical
                    # checkout, not current bytes paired with historical hashes.
                    for name,module in list(__import__('sys').modules.items()):
                        if name.startswith(('test_pe4_', 'test_pe5_', 'test_pe6_', 'test_pe10_')) and module is not None:
                            namespace=vars(module)
                            if namespace.get('ROOT') == repository_root:
                                stack.enter_context(patch.dict(namespace, ROOT=snapshot))
                    for namespace in namespaces:
                        replacement = dict(ROOT=snapshot)
                        if 'git' in namespace:
                            replacement['git'] = namespace_git.get(id(namespace), historical_git)
                        stack.enter_context(patch.dict(namespace, **replacement))
                    return bound_tests.run(result, debug)
    return HistoricalSuite([tests])

class ImplementationGovernanceTests(unittest.TestCase):
    def test_current_implementation_closed_scope_identity_and_protected_objects(self):
        self.assertEqual(implementation_successor()["authorized_paths"],CORRECTION_PATHS)
        self.assertEqual(accepted_implementation()["authorized_paths"],AUTHORIZED_PATHS)
    def test_historical_design_retains_exact_twenty_one_paths(self):
        record=accepted_design()
        self.assertEqual(len(record["authorized_paths"]),21)
        self.assertEqual(set(record["authorized_paths"]),set(git("diff","--name-only","d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221",BASE).decode().splitlines()))
        for item in record["artifacts"]:
            value=historical(item["path"])
            self.assertEqual((sha(value),blob(value)),(item["sha256"],item["git_blob"]))
    def test_original_historical_validator_body_and_scope_check_unchanged(self):
        path="tests/test_pe6_classification_contract_design.py"
        def function(data):
            return next(x for x in ast.parse(data).body if isinstance(x,ast.FunctionDef) and x.name=="validate_design")
        self.assertEqual(ast.dump(function(historical(path)),include_attributes=False),ast.dump(function(raw(path)),include_attributes=False))
    def test_historical_record_identity_cannot_be_refreshed(self):
        record=copy.deepcopy(accepted_design());schema=json.loads(historical(DESIGN_SCHEMA))
        record["artifacts"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_historical_design(record,schema)
        import test_pe6_classification_contract_design as prior
        with self.assertRaises(ValueError):validate_historical_design(record,prior.schema_for(record))
    def test_historical_authorization_cannot_be_expanded_for_successor(self):
        import test_pe6_classification_contract_design as prior
        record=copy.deepcopy(accepted_design());record["authorized_paths"].append("pi4/lib/hioc/classification.py")
        with self.assertRaises(ValueError):validate_historical_design(record,prior.schema_for(record))
    def test_unrelated_untracked_file_is_not_authorized(self):
        original=git
        def extra(*args):
            if args==("ls-files","--others","--exclude-standard"):
                return original(*args)+b"unrelated-private-file.txt\n"
            return original(*args)
        record=copy.deepcopy(implementation_successor())
        with patch.dict(globals(),git=extra),self.assertRaisesRegex(ValueError,"unexpected implementation path"):
            validate_timestamp_correction(record)
    def test_protected_runtime_mutation_is_rejected(self):
        original=raw
        path="pi4/lib/hioc/inventory.py"
        def changed(p):return b"unauthorized" if p==path else original(p)
        record=copy.deepcopy(implementation_successor())
        with patch.dict(globals(),raw=changed),self.assertRaisesRegex(ValueError,"protected baseline artifact"):
            validate_timestamp_correction(record)
    def test_current_and_historical_maps_are_independent(self):
        from test_pe6_classification_contract_design import design_successor,design_binding
        self.assertEqual(design_successor(),accepted_design())
        old=next(x for x in accepted_design()["artifacts"] if x["path"]=="docs/HIOC_MASTER_PLAN.md")
        new=implementation_binding(old["path"])
        self.assertNotEqual(old["sha256"],new["sha256"])
        self.assertEqual(design_binding(old["path"]),new)
        assert_implementation_sequence(raw(old["path"]).decode())
    def test_historical_design_source_record_schema_unchanged(self):
        for path in [DESIGN_RECORD,DESIGN_SCHEMA,DESIGN_DOCUMENT]:
            self.assertEqual(raw(path),historical(path))
    def test_original_five_file_candidate_and_asset_correction_retained(self):
        record=accepted_implementation()
        self.assertEqual(len(record["preserved_candidate_paths"]),5)
        self.assertIn("return parsed, dict(kind=kind",raw("pi4/lib/hioc/classification.py").decode())
        self.assertIn("asset_path.write_bytes(serialize_store(asset()))",raw("tests/test_pe6_classification.py").decode())
        # CLI and contract constants remain byte-identical; reader correction is separately authorized.
        for item in record["preserved_candidate_unmodified"]:
            self.assertEqual(sha(raw(item["path"])),item["sha256"])
            self.assertEqual(sha((ROOT/item["path"]).read_bytes()),item["file_sha256"])
    def test_full_suite_and_no_operational_authority(self):
        record=accepted_implementation()
        self.assertTrue(record["full_native_suite_required"])
        self.assertFalse(record["production_authorized"])
        self.assertFalse(record["pe6_2_started"])
        self.assertEqual(record["operational_facts"],accepted_design()["unresolved_decisions"]["operational_facts"])


    def public_entries(self):
        import test_pe6_classification_contract_design as prior
        text=raw('docs/HIOC_MASTER_PLAN.md').decode()
        return [implementation_successor,
                lambda:implementation_binding('docs/HIOC_MASTER_PLAN.md'),
                lambda:assert_implementation_sequence(text),
                lambda:prior.design_binding('docs/HIOC_MASTER_PLAN.md'),
                lambda:prior.assert_pe6_sequence(text)]

    def test_warm_public_entries_reject_new_unauthorized_path(self):
        implementation_successor();original=git
        def extra(*args):
            if args==('ls-files','--others','--exclude-standard'):
                return original(*args)+b'unauthorized-after-validation.txt\n'
            return original(*args)
        with patch.dict(globals(),git=extra):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'unexpected implementation path'):entry()

    def test_warm_public_entries_reject_protected_mutation(self):
        implementation_successor();original=raw
        def changed(path):return b'unauthorized' if path=='pi4/lib/hioc/inventory.py' else original(path)
        with patch.dict(globals(),raw=changed):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'protected baseline artifact'):entry()

    def test_warm_public_entries_revalidate_record_and_schema(self):
        implementation_successor();original=raw
        for path in (RECORD,SCHEMA):
            changed=json.loads(original(path))
            changed['unexpected_after_warmup']=True
            def replaced(name,path=path,changed=changed):return canonical(changed) if name==path else original(name)
            with self.subTest(path=path),patch.dict(globals(),raw=replaced):
                for entry in self.public_entries():
                    with self.assertRaisesRegex(ValueError,'exact implementation schema'):entry()
        implementation_successor()  # Restored fixture is independently valid.

    def test_warm_public_entries_revalidate_current_artifact(self):
        implementation_successor();original=raw
        def changed(path):return original(path)+b'\n' if path=='docs/DATA_MODEL.md' else original(path)
        with patch.dict(globals(),raw=changed):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'current implementation artifact'):entry()

    def test_warm_public_entries_revalidate_index_object_and_scope(self):
        implementation_successor();original=git
        def changed(*args):
            result=original(*args)
            if args==('ls-files','--stage'):
                rows=result.decode().splitlines()
                for i,row in enumerate(rows):
                    if row.endswith('\tdocs/DATA_MODEL.md'):
                        mode,oid,stage=row.split('\t')[0].split()
                        rows[i]=mode+' '+'0'*40+' '+stage+'\tdocs/DATA_MODEL.md'
                return ('\n'.join(rows)+'\n').encode()
            return result
        with patch.dict(globals(),git=changed):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'current staged artifact'):entry()
        def extra(*args):
            result=original(*args)
            return result+b'unauthorized-index.txt\n' if args==('diff','--cached','--name-only',CORRECTION_BASE) else result
        with patch.dict(globals(),git=extra):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'unexpected staged implementation path'):entry()

    def test_immutable_cache_is_preserved_but_current_design_guard_is_fresh(self):
        first=_accepted_design();self.assertIs(first,_accepted_design())
        exposed=accepted_design();exposed['authorized_paths'].append('forged')
        self.assertNotIn('forged',accepted_design()['authorized_paths'])
        original=raw
        with patch.dict(globals(),raw=lambda path:b'forged' if path==DESIGN_RECORD else original(path)):
            with self.assertRaisesRegex(ValueError,'immutable PE6.0 design authority'):accepted_design()
        self.assertEqual(len(accepted_design()['authorized_paths']),21)



    def test_historical_runtime_guard_accepts_only_exact_pe61_additions(self):
        from test_pe5_service_association_caller import assert_historical_runtime_tree
        assert_historical_runtime_tree('c7db29f795909d7926e36c02f1166034bcebb8b0',['pi4','release','tools','requirements-pe4.lock'])

    def test_historical_runtime_guard_original_statements_and_classes_preserved(self):
        path='tests/test_pe5_service_association_caller.py'
        old,new=ast.parse(historical(path)),ast.parse(raw(path))
        classes=lambda tree:[ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.ClassDef)]
        self.assertEqual(classes(old),classes(new))
        function=lambda tree:next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='assert_historical_runtime_tree')
        prior=[ast.dump(n,include_attributes=False) for n in function(old).body]
        current=[ast.dump(n,include_attributes=False) for n in function(new).body]
        self.assertEqual(len(current),len(prior)+1)
        self.assertEqual([n for n in current if n in prior],prior)

    def test_historical_runtime_guard_cannot_exempt_existing_baseline_file(self):
        import test_pe5_service_association_caller as prior
        original=prior.git
        def existing(*args):
            if args[:3]==('ls-tree','--name-only',BASE) and args[-1].startswith('pi4/'):
                return (args[-1]+'\n').encode()
            return original(*args)
        with patch.object(prior,'git',existing),self.assertRaisesRegex(ValueError,'existing runtime cannot be exempted'):
            prior.assert_historical_runtime_tree('c7db29f795909d7926e36c02f1166034bcebb8b0',['pi4'])



class PE62SuccessorTests(unittest.TestCase):
    def test_original_historical_law_and_test_cases_preserved(self):
        old=ast.parse(accepted_bytes('tests/test_pe6_classification_implementation.py'))
        new=ast.parse(raw('tests/test_pe6_classification_implementation.py'))
        funcs=lambda tree:{x.name:ast.dump(x,include_attributes=False) for x in tree.body if isinstance(x,ast.FunctionDef)}
        for name in ['validate_implementation','validate_historical_design','_accepted_design','accepted_design']:
            self.assertEqual(funcs(old)[name],funcs(new)[name])
        names=lambda tree:{n.name for c in tree.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
        self.assertTrue(names(old)<=names(new))

    def test_pe61_snapshot_retains_original_next_checkpoint_and_identities(self):
        old=accepted_implementation();current=implementation_successor()
        self.assertEqual(old['next_checkpoint'],'PE-6.2 - PI3 Release-Source Synchronization')
        self.assertFalse(old['pe6_2_started']);self.assertFalse(old['runtime_deployment_performed'])
        self.assertEqual(len(old['authorized_paths']),27)
        self.assertEqual(current['authorized_paths'],CORRECTION_PATHS)
        self.assertEqual(current['checkpoint'],'PE-6.4_TIMESTAMP_COMPATIBILITY_CORRECTION')
        self.assertEqual(current['evidence_authority'],'OPERATOR_SUPPLIED')
        self.assertTrue(current['production_deployed']);self.assertFalse(current['production_execution_established']);self.assertFalse(current['pe6_4_started'])
        pe62=accepted_pe62();self.assertEqual(pe62['checkpoint'],'PE-6.2');self.assertFalse(pe62['production_deployed']);self.assertFalse(pe62['pe6_3_started'])
        self.assertIn('### PE-6.2 - PI3 Release-Source Synchronization',accepted_bytes('docs/HIOC_MASTER_PLAN.md').decode())
        assert_implementation_sequence(raw('docs/HIOC_MASTER_PLAN.md').decode())

    def test_replayed_historical_artifact_identity_cannot_be_refreshed(self):
        old=accepted_implementation();old['artifacts'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'current implementation artifact'):
            replay_implementation(old,schema_for(old))
        old=accepted_implementation();old['pe6_2_started']=True
        with self.assertRaisesRegex(ValueError,'implementation-only boundary'):
            replay_implementation(old,schema_for(old))

    def test_current_document_cannot_replace_historical_git_bytes(self):
        original=accepted_bytes;current=raw('docs/HIOC_MASTER_PLAN.md')
        def substituted(path):
            return current if path=='docs/HIOC_MASTER_PLAN.md' else original(path)
        with patch.dict(globals(),accepted_bytes=substituted),self.assertRaisesRegex(ValueError,'current implementation artifact'):
            replay_implementation()

    def reject_rebound_current(self,path,value,reason):
        original_raw,original_git=raw,git
        def changed(p):return value if p==path else original_raw(p)
        def rebound(*args):
            data=original_git(*args)
            if args==('ls-files','--stage'):
                lines=data.decode().splitlines()
                lines=[line.split(' ')[0]+' '+blob(value)+' 0\t'+path if line.endswith('\t'+path) else line for line in lines]
                return ('\n'.join(lines)+'\n').encode()
            return data
        with patch.dict(globals(),raw=changed,git=rebound),self.assertRaisesRegex(ValueError,reason):
            implementation_successor()

    def test_false_completion_and_deployment_rejected_even_if_restaged(self):
        path='docs/HIOC_MASTER_PLAN.md';implementation_successor()
        for before,after in [('PE6_3_STATUS=COMPLETE/PASS','PE6_3_STATUS=NOT_STARTED'),
                             ('PE6_PRODUCTION_DEPLOYED=TRUE','PE6_PRODUCTION_DEPLOYED=FALSE'),
                             ('PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE','PE6_PRODUCTION_EXECUTION_ESTABLISHED=TRUE'),
                             ('PE6_4_STARTED=FALSE','PE6_4_STARTED=TRUE'),
                             ('Separate authorization is required for PE-6.4','PE-6.4 is authorized'),
                             ('OPERATOR_SUPPLIED','CODEX_VERIFIED')]:
            with self.subTest(change=after):
                self.reject_rebound_current(path,raw(path).replace(before.encode(),after.encode()),'PE6.3 exact lifecycle')

    def test_operator_evidence_and_historical_prefix_cannot_be_rewritten(self):
        path='docs/PE6_CLASSIFICATION_IMPLEMENTATION.md'
        for before,after in [(b'inode=654548',b'inode=1'),
                             (b'EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED',b'EVIDENCE_AUTHORITY=DIRECT_OBSERVATION'),
                             (b'# PE-6.1 Private Classification',b'# Changed historical PE-6.1')]:
            with self.subTest(change=after):
                self.reject_rebound_current(path,raw(path).replace(before,after),'PE6.3 exact operator evidence')

    def test_historical_success_does_not_authorize_old_edit_scope(self):
        accepted_implementation();original=git
        def extra(*args):
            data=original(*args)
            if args==('diff','--name-only',CORRECTION_BASE):return data+b'docs/DATA_MODEL.md\n'
            return data
        with patch.dict(globals(),git=extra),self.assertRaisesRegex(ValueError,'unexpected implementation path'):
            implementation_successor()

    def test_current_success_is_not_cached_through_design_entry(self):
        import test_pe6_classification_contract_design as design
        design.design_successor();original=raw
        with patch.dict(globals(),raw=lambda p:b'altered' if p==DESIGN_RECORD else original(p)):
            with self.assertRaisesRegex(ValueError,'immutable PE6.0 design authority'):design.design_successor()

    def test_unmerged_and_wrong_mode_index_rejected(self):
        implementation_successor();original=git
        for field,value in [(0,'100755'),(2,'1')]:
            def changed(*args,field=field,value=value):
                data=original(*args)
                if args==('ls-files','--stage'):
                    lines=data.decode().splitlines()
                    for i,line in enumerate(lines):
                        meta,path=line.split('\t',1)
                        if path=='docs/HIOC_MASTER_PLAN.md':
                            bits=meta.split();bits[field]=value;lines[i]=' '.join(bits)+'\t'+path
                    return ('\n'.join(lines)+'\n').encode()
                return data
            with self.subTest(field=field),patch.dict(globals(),git=changed),self.assertRaises(ValueError):implementation_successor()

    def test_current_lifecycle_text_substitution_rejected(self):
        with self.assertRaisesRegex(ValueError,'current lifecycle text substitution'):
            assert_implementation_sequence(accepted_bytes('docs/HIOC_MASTER_PLAN.md').decode())

    def test_returned_scope_and_index_do_not_mutate_authority(self):
        value=implementation_successor();value['authorized_paths'].append('forged')
        index=accepted_index();index['forged']=['100644','0'*40]
        self.assertNotIn('forged',implementation_successor()['authorized_paths'])
        self.assertNotIn('forged',accepted_index())

    def test_exact_existing_status_section_interface(self):
        full=raw('docs/HIOC_MASTER_PLAN.md').decode()
        status=full.split('# Implementation Status',1)[1].split('# Historical Operator Preparation Chronology',1)[0]
        assert_implementation_sequence(full);assert_implementation_sequence(status)
        for text in [status.replace('PE6_4_STARTED=FALSE','PE6_4_STARTED=TRUE'),
                     status.replace('OPERATOR_SUPPLIED','DIRECT_OBSERVATION'),status+'extra']:
            with self.subTest(text=text[-40:]),self.assertRaisesRegex(ValueError,'current lifecycle text substitution'):
                assert_implementation_sequence(text)


class PE63AcceptanceTests(unittest.TestCase):
    def test_pe61_and_pe62_validator_bodies_and_constants_preserved(self):
        old,new=ast.parse(pe62_bytes('tests/test_pe6_classification_implementation.py')),ast.parse(raw('tests/test_pe6_classification_implementation.py'))
        funcs=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
        for name in ['validate_implementation','replay_implementation','accepted_implementation','validate_pe62','expected_master','accepted_bytes','accepted_index']:
            self.assertEqual(funcs(old)[name],funcs(new)[name])
        literals=lambda tree:{t.id:ast.dump(n.value,include_attributes=False) for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
        for name in ['ACCEPTED_IMPLEMENTATION','PE62_BASE','PE62_PATHS','PE62_CURRENT','PE62_STATUS','PE62_REPORT']:
            self.assertEqual(literals(old)[name],literals(new)[name])
        tests=lambda tree:{n.name for c in tree.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
        self.assertTrue(tests(old)<=tests(new))

    def test_three_distinct_checkpoint_authorities(self):
        pe61=accepted_implementation();pe62=accepted_pe62();current=implementation_successor()
        self.assertEqual(pe61['next_checkpoint'],'PE-6.2 - PI3 Release-Source Synchronization')
        self.assertFalse(pe61['runtime_deployment_performed'])
        self.assertEqual(pe62['checkpoint'],'PE-6.2');self.assertEqual(pe62['authorized_paths'],PE62_PATHS)
        self.assertFalse(pe62['production_deployed']);self.assertFalse(pe62['pe6_3_started'])
        self.assertEqual(current['checkpoint'],'PE-6.4_TIMESTAMP_COMPATIBILITY_CORRECTION');self.assertEqual(current['authorized_paths'],CORRECTION_PATHS)
        self.assertTrue(current['production_deployed']);self.assertFalse(current['production_execution_established'])
        self.assertFalse(current['pe6_4_started']);self.assertFalse(current['scheduler_authorized'])
        self.assertEqual(current['evidence_authority'],'OPERATOR_SUPPLIED')

    def test_historical_pe62_false_identities_scope_or_deployment_rejected(self):
        for field in ['sha','scope','deployment']:
            record=accepted_pe62()
            if field=='sha':record['artifacts'][0]['sha256']='0'*64
            elif field=='scope':record['authorized_paths'].append('pi4/lib/hioc/inventory.py')
            else:record['production_deployed']=True
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'exact current PE6.2 successor'):replay_pe62(record)

    def test_current_document_cannot_replace_pe62_git_snapshot(self):
        original=pe62_bytes;current=raw('docs/HIOC_MASTER_PLAN.md')
        def substituted(path):return current if path=='docs/HIOC_MASTER_PLAN.md' else original(path)
        with patch.dict(globals(),pe62_bytes=substituted),self.assertRaises(ValueError):replay_pe62()

    def test_both_historical_documents_and_sections_cannot_be_current(self):
        for reader in [accepted_bytes,pe62_bytes]:
            full=reader('docs/HIOC_MASTER_PLAN.md').decode()
            status=full.split('# Implementation Status',1)[1].split('# Historical Operator Preparation Chronology',1)[0]
            for text in [full,status]:
                with self.subTest(reader=reader.__name__,form=len(text)),self.assertRaisesRegex(ValueError,'current lifecycle text substitution'):
                    assert_implementation_sequence(text)

    def test_current_record_cannot_claim_execution_activation_or_wrong_deployment(self):
        for field,value in [('production_execution_established',True),('pe6_4_started',True),('scheduler_authorized',True),('production_deployed',False),('evidence_authority','DIRECT_OBSERVATION')]:
            record=implementation_successor();record[field]=value
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'exact current PE6.3 successor'):validate_timestamp_correction(record)

    def test_report_false_installation_permissions_identity_or_runtime_equivalence_rejected(self):
        path='docs/PE6_CLASSIFICATION_IMPLEMENTATION.md'
        for before,after in [('mode 0600','mode 0644'),('UID:GID 1000:1000','UID:GID 0:0'),
                             ('df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503','4dad543d46c62a3335776d239f983082574361979200379990cf6c2ddfa3fb7e'),
                             ('ROLLBACK=NOT_PERFORMED','ROLLBACK=PASS'),('EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED','EVIDENCE_AUTHORITY=DIRECT_OBSERVATION')]:
            self.assertIn(before,PE63_REPORT)
            value=pe62_bytes(path)+PE63_REPORT.replace(before,after).encode()
            with self.subTest(change=after):PE62SuccessorTests.reject_rebound_current(self,path,value,'PE6.3 exact operator evidence')

    def test_prior_pe62_scope_is_not_current_edit_authority(self):
        implementation_successor();original=git
        def extra(*args):
            data=original(*args)
            if args==('diff','--name-only',CORRECTION_BASE):return data+b'tests/test_pe6_classification_contract_design.py\n'
            return data
        with patch.dict(globals(),git=extra),self.assertRaisesRegex(ValueError,'unexpected implementation path'):validate_timestamp_correction()

    def test_old_pe62_design_test_file_is_now_protected(self):
        path='tests/test_pe6_classification_contract_design.py'
        PE62SuccessorTests.reject_rebound_current(self,path,raw(path)+b'\n','current implementation artifact')

    def test_current_warm_undeclared_path_untracked_and_wrong_parent_rejected(self):
        implementation_successor();original=git
        cases=[(('ls-files','--others','--exclude-standard'),b'foreign.txt\n','unexpected implementation path'),
               (('branch','--show-current'),b'other\n','current branch'),
               (('rev-parse','origin/main'),b'0'*40+b'\n','current publication provenance')]
        for command,value,reason in cases:
            def changed(*args,command=command,value=value):return value if args==command else original(*args)
            with self.subTest(command=command),patch.dict(globals(),git=changed),self.assertRaisesRegex(ValueError,reason):implementation_successor()
        def parent(*args):
            if args==('rev-parse','HEAD'):return b'f'*40+b'\n'
            if args==('show','-s','--format=%P','f'*40):return b'0'*40+b'\n'
            return original(*args)
        with patch.dict(globals(),git=parent),self.assertRaisesRegex(ValueError,'current checkpoint parent'):implementation_successor()

    def test_returned_pe62_history_and_index_cannot_mutate_later_authority(self):
        historical_record=accepted_pe62();historical_record['authorized_paths'].append('forged')
        index=pe62_index();index['forged']=['100644','0'*40]
        self.assertNotIn('forged',accepted_pe62()['authorized_paths']);self.assertNotIn('forged',pe62_index())

    def test_exact_current_full_and_status_forms_reject_modified_sections(self):
        full=raw('docs/HIOC_MASTER_PLAN.md').decode();status=full.split('# Implementation Status',1)[1].split('# Historical Operator Preparation Chronology',1)[0]
        assert_implementation_sequence(full);assert_implementation_sequence(status)
        for text in [status.replace('PE6_4_STARTED=FALSE','PE6_4_STARTED=TRUE'),status.replace('PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE','PE6_PRODUCTION_EXECUTION_ESTABLISHED=TRUE'),status+'unexpected']:
            with self.assertRaisesRegex(ValueError,'current lifecycle text substitution'):assert_implementation_sequence(text)

    def test_four_installed_source_digests_match_accepted_git_objects(self):
        self.assertEqual(len(PE63_INSTALLED),4)
        for path,digest in PE63_INSTALLED.items():
            self.assertEqual(sha(pe62_bytes(path)),digest);self.assertEqual(pe63_bytes(path),pe62_bytes(path))
            if path!="pi4/lib/hioc/classification.py":self.assertEqual(raw(path),pe63_bytes(path))

class TimestampSuccessorTests(unittest.TestCase):
    def test_original_pe63_law_constants_and_all_case_names_preserved(self):
        old,new=ast.parse(pe63_bytes("tests/test_pe6_classification_implementation.py")),ast.parse(raw("tests/test_pe6_classification_implementation.py"))
        funcs=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef)}
        for name in ["validate_implementation","validate_pe62","validate_pe63","expected_pe63_master","replay_pe62"]:
            self.assertEqual(funcs(old)[name],funcs(new)[name])
        literals=lambda t:{x.id:ast.dump(n.value,include_attributes=False) for n in t.body if isinstance(n,ast.Assign) for x in n.targets if isinstance(x,ast.Name)}
        for name in ["PE63_BASE","PE63_PATHS","PE63_CURRENT","PE63_STATUS","PE63_REPORT","PE63_INSTALLED"]:
            self.assertEqual(literals(old)[name],literals(new)[name])
        cases=lambda t:{n.name for c in t.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith("test_")}
        self.assertTrue(cases(old)<=cases(new))

    def test_historical_pe63_identity_scope_and_execution_cannot_be_refreshed(self):
        self.assertEqual(accepted_pe63()["checkpoint"],"PE-6.3")
        self.assertEqual(accepted_pe63()["authorized_paths"],PE63_PATHS)
        for change in ["identity","scope","execution"]:
            record=accepted_pe63()
            if change=="identity":record["artifacts"][0]["sha256"]="0"*64
            elif change=="scope":record["authorized_paths"].append("pi4/lib/hioc/classification.py")
            else:record["production_execution_established"]=True
            with self.subTest(change=change),self.assertRaises(ValueError):replay_pe63(record)

    def test_current_bytes_cannot_substitute_historical_pe63(self):
        original=pe63_bytes;current=raw("pi4/lib/hioc/classification.py")
        with patch.dict(globals(),pe63_bytes=lambda p:current if p=="pi4/lib/hioc/classification.py" else original(p)):
            with self.assertRaises(ValueError):replay_pe63()

    def test_corrected_source_rebinding_and_false_deployment_rejected(self):
        path="pi4/lib/hioc/classification.py"
        PE62SuccessorTests.reject_rebound_current(self,path,raw(path)+b"\n","exact corrected source/test identity")
        record=implementation_successor();record["corrected_artifact_deployment_established"]=True
        with self.assertRaises(ValueError):validate_timestamp_correction(record)

    def test_all_prior_master_snapshots_rejected_as_current(self):
        for reader in [accepted_bytes,pe62_bytes,pe63_bytes]:
            full=reader("docs/HIOC_MASTER_PLAN.md").decode()
            with self.assertRaisesRegex(ValueError,"current lifecycle text substitution"):assert_implementation_sequence(full)


if __name__=="__main__":unittest.main()
