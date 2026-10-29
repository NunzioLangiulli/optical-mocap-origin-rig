# SPDX-License-Identifier: MIT
"""Package a checked source/model repository without local environments or Git metadata."""
import hashlib,zipfile
from check_repository import ROOT,main as check,project_files

if __name__=='__main__':
    check()
    out=ROOT/'dist'; out.mkdir(exist_ok=True)
    path=out/'optical-mocap-origin-rig-v0.2.0-design-v7.zip'
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for source in project_files():
            archive.write(source,'optical-mocap-origin-rig/'+source.relative_to(ROOT).as_posix())
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    path.with_suffix('.zip.sha256').write_text(f'{digest}  {path.name}\n',encoding='utf-8')
    print(f'Created {path.name} ({path.stat().st_size:,} bytes).')
