# SPDX-License-Identifier: MIT
"""Offline checks: links, English asset set, licenses, hashes and private-path exclusion."""
import hashlib,json,re
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','.venv','venv','build','dist','__pycache__','.pytest_cache'}

def project_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(ROOT).parts))

def main():
    failures=[]
    files=project_files()
    for p in files:
        if p.suffix in {'.md','.py','.txt','.json','.yml','.csv'} or p.name in {'LICENSE','.gitignore','.gitattributes'}:
            text=p.read_text(encoding='utf-8')
            # Detect accidental workstation paths without embedding one in this checker.
            if re.search(r'[A-Za-z]:[\\/]Users[\\/]',text): failures.append(f'Personal absolute path: {p.relative_to(ROOT)}')
            if p.suffix=='.md':
                for raw in re.findall(r'\]\(([^)]+)\)',text):
                    url=raw.split(' "',1)[0].strip('<>')
                    if urlsplit(url).scheme or url.startswith('#'): continue
                    local=unquote(url.split('#',1)[0])
                    if local and not (p.parent/local).exists(): failures.append(f'Broken link in {p.relative_to(ROOT)}: {local}')
    for name in ['LICENSE','LICENSES/MIT.txt','LICENSES/CC-BY-4.0.txt','validation/geometry_report.json','docs/images/origin-rig-v7.png','docs/images/underside-and-rear.png']:
        if not (ROOT/name).is_file(): failures.append(f'Missing required file: {name}')
    hashes=ROOT/'validation'/'SHA256SUMS.txt'
    if not hashes.exists(): failures.append('Missing asset hashes')
    else:
        for line in hashes.read_text(encoding='utf-8').splitlines():
            expected,name=line.split('  ',1); path=ROOT/name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected: failures.append(f'Hash mismatch: {name}')
    report_path=ROOT/'validation'/'geometry_report.json'
    if report_path.exists():
        report=json.loads(report_path.read_text(encoding='utf-8'))
        for name,metrics in report['models'].items():
            path=ROOT/'models'/(name+'.stl')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=metrics['sha256']: failures.append(f'Stale report: {name}')
    if failures: raise SystemExit('\n'.join(failures))
    print(f'PASS: {len(files)} project files; local links, required assets, licenses and hashes checked.')

if __name__=='__main__': main()
