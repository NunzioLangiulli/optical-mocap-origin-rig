# Building and maintaining the project

## Layout

```text
src/origin_rig.py             standalone v7 geometry and STL validation
scripts/build.py              reproducible build entry point
scripts/render_preview.py     portable STL-based preview renderer
scripts/audit_release.py      released-file metrics and rebuild comparison
scripts/check_repository.py   local links, asset hashes and packaging checks
scripts/package_release.py    creates a clean source/model ZIP
models/                       three printable reference STL files
docs/                         English design and user documentation
validation/                   digital report, hashes and physical-test template
tests/                        geometry regression checks
.github/                      workflow and issue templates
LICENSES/                     full license texts
```

No earlier revision, personal dependency folder, proprietary Vicon document, printer credential or G-code is needed to build this project. The original iterative CAD files have been consolidated into one module rather than copied as a chain of imports.

## Python environment

The reference build used Python 3.12. Exact package versions are in `requirements.txt`. These pins describe the tested local toolchain, not a promise of compatibility with every future Python/platform combination.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS/Linux:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If environment activation is restricted, run the environment's Python executable directly. Do not change system policy solely for this project.

## Build and inspect

```sh
python scripts/build.py
python -m unittest discover -s tests -v
python scripts/render_preview.py
python scripts/audit_release.py
python scripts/check_repository.py
python scripts/package_release.py
```

`build.py` writes to ignored `build/`, including a machine-readable report. It does not replace the reference models. Rendering uses the tracked STL and Pillow's bundled font, with no platform-specific font path. The coloured markers are illustrative and are not exported in the printable files.

`audit_release.py` deliberately updates the tracked validation report and hashes; use it when preparing a release. Review these changes before committing. The packaging script checks the repository first and excludes development environments, caches, build output and Git metadata. It creates an archive in ignored `dist/`.

## Thread adjustment

```sh
python scripts/build.py --thread-clearance 0.25 --output build/clearance-025
```

This changes the **radial** allowance from 0.20 to 0.25 mm; diameters increase by 0.10 mm relative to the default. It rebuilds both rig and thread coupon consistently. Test the new coupon before adopting its rig. The published tests target the default geometry, not a customised clearance.

Do not scale the whole STL to adjust thread fit: this also moves the marker faces and changes the 150 mm distances. A material shrinkage compensation should be based on measured behaviour and documented separately.

## Other geometry changes

The current model is a fixed 150 mm reference design, not a fully general configurable rig. Changing one numeric constant does not necessarily update every dependent feature. For a different span, marker base or mounting scheme, update the geometry, declared marker coordinates, regression tests, documentation and validation evidence together.

Boolean solids use millimetres. The final mesh simplifier operates at 0.02 mm tolerance. Exported float32 STL triangulations may differ across library versions; compare geometry and retain the exact released STL hashes for traceability.

## Review and release

Keep physical claims separate from digital checks. Run tests after meaningful geometry changes, inspect new preview images, audit files and update the design revision/changelog. Do not label a release “print-tested” unless an actual print record and result are included. The first suggested software release is `v0.2.0`, containing design revision `v7`; these labels refer to different histories.

See [publishing](publishing.md) for the prepared GitHub metadata and upload procedure.
