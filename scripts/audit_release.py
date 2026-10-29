# SPDX-License-Identifier: MIT
"""Update digital evidence for the tracked models; does not perform physical validation."""
import hashlib,json,platform,subprocess,sys
from pathlib import Path
from importlib.metadata import version
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import origin_rig as rig
import numpy as np
import trimesh

def main():
    run=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,text=True,capture_output=True)
    log=run.stdout+run.stderr
    if run.returncode:
        print(log); raise SystemExit(run.returncode)
    target=ROOT/'validation'; target.mkdir(exist_ok=True)
    (target/'local-test-results.txt').write_text(log,encoding='utf-8')
    report={'design_revision':'v7','evidence_type':'digital only','units':'mm',
      'python':platform.python_version(),'packages':{n:version(n) for n in ['numpy','manifold3d','trimesh','Pillow']},
      'local_geometry_tests':'passed','remote_github_actions':'not observed',
      'pad_centres_mm':rig.ALL_PAD_CENTRES.tolist(),'models':{},
      'physical_status':{k:'not tested' for k in ['slicing','ABS_coupons','full_print','dimensional_accuracy','mechanical_stiffness','marker_visibility','Nexus_use','Motive_use']}}
    for path in sorted((ROOT/'models').glob('*.stl')):
        metrics=rig.mesh_metrics(trimesh.load_mesh(path))
        metrics['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        report['models'][path.stem]=metrics
    ref=trimesh.load_mesh(ROOT/'models'/'origin_rig_v7.stl')
    solid=rig.models()['origin_rig_v7']; mesh=rig.cleaned_mesh(solid)
    refsolid=rig.md.Manifold(rig.md.Mesh(np.asarray(ref.vertices,dtype=np.float32),np.asarray(ref.faces,dtype=np.uint32)))
    report['rebuild_comparison']={'absolute_volume_difference_mm3':float(abs(mesh.volume-ref.volume)),
      'symmetric_difference_mm3':float((solid-refsolid).volume()+(refsolid-solid).volume()),
      'thresholds_mm3':{'absolute_volume_difference':10,'symmetric_difference':30},
      'note':'Boolean triangulation/simplification may differ. Reference STL files remain unchanged.'}
    (target/'geometry_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    assets=sorted([*(ROOT/'models').glob('*.stl'),*(ROOT/'docs'/'images').glob('*.png')])
    hashes=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n' for p in assets)
    (target/'SHA256SUMS.txt').write_text(hashes,encoding='utf-8')
    print(log)
    print(json.dumps(report['rebuild_comparison'],indent=2))

if __name__=='__main__': main()
