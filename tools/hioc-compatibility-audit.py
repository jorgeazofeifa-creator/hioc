#!/usr/bin/env python3
"""Read-only repository dependency inventory. Never executes discovered commands."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SIGNALS = {
    "version_or_pin": r"(?:version|VERSION|Version|CORE_TAG|SOABI|WHEEL|ExpectedMajorMinor|ExpectedPythonMajorMinor).*?(?:==|!=|=|-cne|-eq|:[^ ]*|[0-9]\.[0-9])",
    "trust_identity": r"[0-9a-fA-F]{40,64}|Authenticode|StrictHostKeyChecking|known_hosts",
    "external_shape": r"subprocess\.|run_command\(|\bcommand -v\b|Get-Command|Invoke-Native|\.split\(|\.recv\(|urlopen|/api/|state_topic|/etc/|/proc/|/sys/|dir_fd|fsync",
}


def audit(root=ROOT):
    registry=json.loads((root/'governance/compatibility-contracts.json').read_text(encoding='utf-8'))
    patterns={d['dependency_id']:[re.compile('|'.join(d['audit_patterns']),re.I)] for d in registry['dependencies']}
    classes={d['dependency_id']:d['dependency_class'] for d in registry['dependencies']}
    policy={d['dependency_id']:d['policy'] for d in registry['dependencies']}
    files=sorted(set(subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=root,text=True).splitlines()))
    excludes={'governance/compatibility-audit.json','docs/COMPATIBILITY_RESILIENCE.md','governance/compatibility-contracts.json'}
    coverage=[]; findings=[]; unresolved=[]; pins=[]; imports=[]; call_sites=[]
    for name in files:
        path=root/name
        if name in excludes or not path.is_file(): continue
        raw=path.read_bytes()
        try:text=raw.decode('utf-8-sig')
        except UnicodeError:
            coverage.append({'path':name,'review':'BINARY_OR_NON_UTF8','sha256':hashlib.sha256(raw).hexdigest()});continue
        deps=set()
        for line_number,line in enumerate(text.splitlines(),1):
            # Include release observations in tables/prose even when the line
            # does not contain a variable named version. Numeric candidates
            # remain candidates (timeouts are not software release gates).
            numeric_literals=sorted(set(re.findall(r'(?<![\w.])[0-9]{1,4}\.[0-9]{1,3}(?:\.[0-9]{1,3})?(?![\w.])',line)))
            matched=[identifier for identifier,rules in patterns.items() if any(r.search(line) for r in rules)]
            deps.update(matched)
            categories=[key for key,pattern in SIGNALS.items() if re.search(pattern,line)]
            if numeric_literals and "version_or_pin" not in categories:
                categories.append("version_or_pin")
            if categories:
                # Standard-library/internal parsers use the governed runtime and
                # internal schema contract; external-specific matches retain IDs.
                assigned=matched or (['system_python'] if name.endswith('.py') else ['internal_schemas'] if name.endswith(('.json','.yaml','.md')) else ['linux_utils'])
                findings.append({'path':name,'line':line_number,'categories':categories,'dependencies':assigned})
                if 'version_or_pin' in categories or 'trust_identity' in categories:
                    tokens=numeric_literals
                    pins.append({'path':name,'line':line_number,'numeric_version_literals':tokens,'exact_identity_literals':sorted(set(re.findall(r'(?<![0-9a-fA-F])[0-9a-fA-F]{40,64}(?![0-9a-fA-F])',line))),'dependencies':assigned,
                        'classification':sorted(set(policy[d] for d in assigned)),
                        'context':'HISTORICAL_OR_SYNTHETIC' if name.startswith(('tests/','docs/','governance/')) or name.endswith('.md') else 'EXECUTABLE_CONTRACT'})
        if name.endswith('.py'):
            try:tree=ast.parse(text)
            except SyntaxError:tree=None
            for node in ast.walk(tree) if tree else []:
                if isinstance(node,(ast.Import,ast.ImportFrom)):
                    names=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or 'relative']
                    for module in names:
                        identifier='pe4_websockets' if module.split('.')[0]=='websockets' else 'pyyaml' if module.split('.')[0]=='yaml' else 'internal_schemas' if module.split('.')[0]=='hioc' else 'system_python'
                        imports.append({'path':name,'line':node.lineno,'module':module,'dependency_id':identifier});deps.add(identifier)
                if isinstance(node,ast.Call):
                    func=ast.unparse(node.func)
                    if func.startswith('subprocess.') or func in {'run_command','run','C.run','COMMON.run','H.run'}:
                        executable=None
                        if node.args and isinstance(node.args[0],(ast.List,ast.Tuple)) and node.args[0].elts and isinstance(node.args[0].elts[0],ast.Constant):
                            value=node.args[0].elts[0].value
                            if type(value) is str:executable=value
                        mapped={'ip':'iproute','ss':'iproute','arp':'nettools','git':'git','bash':'bash','ping':'ping','snmpget':'snmp','dpkg-query':'dpkg','systemctl':'systemd','rsync':'rsync','vcgencmd':'linux_metrics','powershell.exe':'powershell','cmd.exe':'powershell','mosquitto_sub':'mqtt_cli','mosquitto_pub':'mqtt_cli','cat':'linux_utils','ssh':'openssh_protocol','ssh.exe':'openssh_protocol','ssh-keygen.exe':'openssh_trust'}
                        identifier=mapped.get(Path(executable).name if executable else '', 'pe4_python' if executable == './bin/python' else 'system_python' if executable and 'python' in executable else 'linux_utils' if executable else 'system_python')
                        call_sites.append({'path':name,'line':node.lineno,'executable':executable,'dependency_id':identifier,'resolution':'STATIC' if executable else 'DYNAMIC_CALLER_CONTRACT'});deps.add(identifier)
        coverage.append({'path':name,'review':'SCANNED_AND_CLASSIFIED','dependencies':sorted(deps),'sha256':hashlib.sha256(raw).hexdigest()})
    return {'schema_version':'1.0','baseline':'2c339bb3a597aaae152c3fb684c11b96eed9bfe9','scope':'ALL_GIT_TRACKED_AND_NONIGNORED_PREPARATION_FILES','coverage':coverage,'findings':findings,'pin_inventory':pins,'python_imports':imports,'process_call_sites':call_sites,'unclassified_dependencies':unresolved,'limitations':['STATIC_REPOSITORY_AUDIT_NOT_LIVE_DEPENDENCY_CERTIFICATION','PATTERN_CLASSIFICATION_IS_AN_INDEX_FOR_MANUAL_REVIEW_NOT_A_PROOF_OF_EXHAUSTIVENESS','UTILITY_AND_STDLIB_FALLBACKS_REQUIRE_MANUAL_CALLER_REVIEW','DYNAMIC_DISPATCH_REQUIRES_GOVERNED_EXECUTION_PROBE','HISTORICAL_EVIDENCE_AND_SYNTHETIC_TEST_CONSTANTS_ARE_NOT_CURRENT_EXTERNAL_VERSION_GATES']}


if __name__=='__main__':
    result=audit()
    if sys.argv[1:]==['--write']:
        (ROOT/'governance/compatibility-audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    elif sys.argv[1:]:raise SystemExit('Only --write is supported')
    print(json.dumps({'files':len(result['coverage']),'classified_findings':len(result['findings']),'pin_sites':len(result['pin_inventory']),'imports':len(result['python_imports']),'process_call_sites':len(result['process_call_sites']),'unclassified':len(result['unclassified_dependencies'])},sort_keys=True))
