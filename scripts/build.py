# SPDX-License-Identifier: MIT
"""Build and validate the three printable models; defaults never overwrite tracked STLs."""
import argparse,hashlib,json,platform,sys
from importlib.metadata import version
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import origin_rig as rig

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'build')
    parser.add_argument('--thread-clearance',type=float,default=.20,help='RADIAL print clearance in mm; default 0.20')
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    report={'design_revision':'v7','units':'mm','radial_thread_clearance_mm':args.thread_clearance,
      'python':platform.python_version(),'packages':{n:version(n) for n in ['numpy','manifold3d','trimesh']},
      'pad_centres_mm':rig.ALL_PAD_CENTRES.tolist(),'models':{},
      'validation_scope':'Digital geometry and exported mesh only. No slicing, physical print, stiffness or acquisition-system validation.'}
    for name,solid in rig.models(args.thread_clearance).items():
        target=args.output/(name+'.stl')
        metrics=rig.export_stl(solid,target)
        metrics['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        report['models'][name]=metrics
    (args.output/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
