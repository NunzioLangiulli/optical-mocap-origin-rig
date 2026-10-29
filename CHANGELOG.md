# Changelog

## 0.2.0 — design v7, 2026-10-28

- Added cylindrical M100 pedestal at (100,0,24) mm.
- One full-rig STL for Vicon 150 mm references and Motive 100/150 mm square.
- Preserved envelope, channels and socket; updated tests, previews and instructions.
- Physical validation remains pending.


## 0.1.0 — prepared for first publication, 2026-10-28

This is the first repository package, containing **design revision v6**. It is not a claim that a GitHub release has already been published.

- Published-ready STL set: rig, pointed-roof coupon and minimal thread coupon.
- Consolidated standalone CAD generator, configurable radial thread allowance and digital checks.
- English design, manufacturing, Nexus workflow, validation and development documentation.
- English previews rendered from the reference STL, asset hashes and physical-test record template.
- MIT license for code; CC BY 4.0 for design and documentation.
- Digital prototype status retained: no confirmed slicing, physical print, mechanical or Nexus result.

## Design history before repository preparation

| Design | Main change |
| --- | --- |
| Initial | Bulky single-body 150 mm rig; printed-thread and captive-nut options |
| Lightweight | Open upper arm channels and a windowed tower to reduce material |
| v3 | Channels moved underneath; marker-foot pockets closed; continuous rear tower channel |
| v4 | Horizontal channels changed to 60° pointed roofs |
| v5 | Marker cones and upper bracket changed to 60°; top-pad side lip removed |
| v6 | Lower cones replaced with constant-diameter Ø18 mm cylindrical supports |

Only v6 is included as a supported reference model. Earlier design choices are described to explain trade-offs, not offered as equally validated alternatives.

### Cross-system documentation update — 2026-10-28

- Adopted the public name Optical Motion-Capture Origin Rig and suggested repository name `optical-mocap-origin-rig`.
- Added sourced OptiTrack/Motive limitations, a system compatibility matrix and a labelled-coordinate reference-frame method.
- Kept all three released STL files and CAD geometry unchanged. No new physical or acquisition-system validation is claimed.
