# Design and nominal geometry

## Coordinate convention

The CAD uses millimetres and a right-handed coordinate system: X and Y lie in the build plate; Z points up. These coordinates describe the **centres of the flat mounting faces**, before markers are attached.

| Mount | X | Y | Z | Function |
| --- | ---: | ---: | ---: | --- |
| O | 0 | 0 | 24 | Origin marker |
| X | 150 | 0 | 24 | Positive X direction |
| Y | 0 | 150 | 24 | Additional positive Y reference |
| Z | 0 | 0 | 174 | Positive Z direction |
| M100 | 100 | 0 | 24 | Intermediate position for Motive |

If every marker has the same centre height `h` above its adhesive surface, its physical centre is the listed point plus `(0, 0, h)`. This common offset cancels in O-to-marker vectors. The nominal vectors are therefore `(150,0,0)`, `(0,150,0)`, and `(0,0,150)` regardless of `h`. This does **not** hold if marker types, mounting orientations, adhesive thicknesses or centring differ.

Rendered 12 mm spheres use `h = 6 mm` for illustration only. The real markers have not been inspected; do not infer their shape, base diameter, visibility or optical centre from a render.

## Envelope and mounting faces

The full solid spans X = −32…159, Y = −15…159 and Z = 0…174 mm. Its envelope is 191 × 174 × 174 mm. On a nominal 256 mm X1E plate this also leaves geometric room for an 8 mm brim when centred, but the slicer must check the actual usable plate and auxiliary features.

All five adhesive faces are Ø18 mm. At X, Y and M100, a solid cylindrical pedestal rises 12 mm above the 12 mm-high arm. At O, the exposed cylinder rises 8 mm above the 16 mm central boss. These constant-diameter supports eliminate the overhangs of earlier cone-shaped supports. They may obstruct low-elevation camera views, especially with flat or hemispherical markers; verify visibility in the installed camera layout.

## Horizontal arms and pointed channels

Each arm is nominally 18 mm wide and 12 mm high. The underside channel runs from coordinate 16 to 141 mm along the arm, leaving the central joint and marker foot closed. It is 10 mm wide at the opening, with 1 mm vertical walls before the two inclined faces start.

The two roof faces rise at **60° from the horizontal build plate**, or **30° from vertical**. Their apex is at:

```text
apex height = 1 + 5 × tan(60°) = 9.6603 mm
material above apex = 12 − 9.6603 = 2.3397 mm
```

The v3 flat 4.4 mm bridge was removed. At a 0.16 mm layer height, the theoretical lateral advance is `0.16 / tan(60°) = 0.0924 mm` per layer. Relative to a hypothetical 0.42 mm extrusion width, that gives approximately 78% geometric overlap. This calculation is **not a layer-strength estimate**. The last closing layer is discretised by the slicer and can still contain a small bridging toolpath.

## Tower and upper bracket

The tower is offset to X = −32…−16 mm, with Y = −8…8 mm. A continuous channel opens to the rear (negative X), leaving nominal 3 mm front and side walls. There are no diamond-shaped windows. The rear channel closes with a pointed arch rather than a flat ceiling.

The upper bracket brings the marker face back to X = 0, directly above O. Its front underside rises 43.301 mm for a 25 mm horizontal advance, giving 60° in the X–Z section. It begins at Z ≈127.899 mm. The upper plate is 18 mm wide, matching the Ø18 mm marker pad, and is backed across the pad footprint. The pad top remains at Z = 174 mm.

The bracket cannot simply be removed or the marker shifted back onto the tower without changing the O–Z vector. Such a change would require a new coordinate design and validation.

## Tripod connection

The central boss is Ø30 × 16 mm. Its bottom socket follows a right-handed 1/4-20 UNC-style printed profile:

- Nominal diameter: 6.35 mm.
- Pitch: 25.4/20 = 1.27 mm.
- Blind depth: 11 mm from the underside.
- Radial FDM allowance: 0.20 mm by default, increasing both diameters by 0.40 mm.
- Entry chamfer and truncated helical profile are included in the cutting solid.

This is not a metrologically gauged or certified thread class. It is not M6. Check the actual tripod screw projection and test hand engagement on the matching coupon. Do not bottom the screw out in the blind hole or force an incompatible screw. PLA trials do not validate the same fit in ABS.

## Material-saving trade-offs

The released v7 mesh has a solid geometric volume of approximately 101.35 cm³, versus approximately 152.84 cm³ for the original bulky design: about 33.7% less solid volume. Intermediate versions were lighter, but exposed upward-facing dust pockets, conical overhangs or undesired openings. V7 favours closed upper surfaces and simple marker supports.

These are mesh-volume comparisons, not measured filament savings. Perimeters, infill, brim, purge and slicer settings determine actual consumption. Open channels also change torsional stiffness; no finite-element or physical stiffness claim is made.

## Coordinate conventions across systems

O/X/Y/Z are this design's labels in a right-handed Z-up frame. They do not configure acquisition software. See [compatibility](compatibility.md) for frame construction and a proper Y-up rotation, and [OptiTrack](optitrack-workflow.md) for marker subsets and origin setup. Revision v7 adds only the M100 cylindrical pedestal to the v6 mechanical design. Its base overlaps the existing arm roof; the pointed underside channel remains open. The extra solid volume is approximately 3.03 cm³, not a slicer filament estimate.
