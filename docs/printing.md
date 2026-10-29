# Printing and assembly

## Required parts

| Item | Quantity | Notes |
| --- | ---: | --- |
| Printed rig | 1 | `models/origin_rig_v7.stl` |
| Identical reflective adhesive markers | 3 for Motive square; 4 for Vicon with Y check | Nominal 12 mm; verify real base fits the Ø18 mm face |
| Bambu ABS black | As sliced | Print quantity and time have not been measured |
| Tripod/plate with compatible male screw | 1 | 1/4-20 UNC, suitable projection for an 11 mm blind socket |
| Same adhesive under every marker | As needed | Avoid different thicknesses or tilted placement |
| Caliper/ruler and a suitable square/level | As available | Choose instruments appropriate to your acceptance criteria |

No metal nut or insert is required in this revision. The socket is printed directly in the body. A nut-pocket variant from early development is not part of this release.

## First: check compatibility

Confirm marker base size and attachment type. “12 mm marker” may describe the reflective part rather than the adhesive base. The mounting face is flat and has no locating recess. Centre markers accurately using a removable alignment aid or measurement; do not assume that the adhesive automatically centres them.

Check that the tripod plate bears stably on the underside central boss and does not foul the arms. Account for anti-rotation pins, screw length and plate shape. The design was not matched to a measured tripod plate.

## Starting slicer settings

These are **proposed starting settings, not a validated print profile**. No printer-specific G-code or ready-to-print 3MF is supplied.

| Setting | Starting point |
| --- | --- |
| Printer | Bambu Lab X1E |
| Nozzle assumption | 0.4 mm |
| Filament | Bambu ABS, black |
| Scale / units | 100% / millimetres |
| Orientation | Supplied orientation: base on plate, tower vertical |
| Layer height | 0.16 mm |
| Wall loops | 4 |
| Top / bottom shell layers | 5 / 5 |
| Sparse infill | 15% gyroid |
| Full-rig brim | 8 mm, check plate fit |
| Supports | Inspect first; do not fill all channels automatically |
| Temperature and cooling | Current material/plate profile, checked for this printer |

Keep the enclosure closed and follow the material manufacturer's preparation, drying and workplace ventilation guidance. Bambu identifies enclosure and brim as measures to reduce ABS warping; these do not establish the accuracy of this particular rig. See [references](references.md).

Do not reuse the early PLA instruction to leave active chamber heating off as an ABS requirement. Conversely, do not invent a chamber temperature independent of the installed X1E/material profile. Avoid increasing general cooling simply to improve an overhang at the expense of ABS layer bonding.

## Coupon sequence

### Thread coupon

The Ø12 × 12 mm coupon reproduces the rig socket, with an 11 mm cavity and 1 mm roof. Print it in the supplied orientation with the same material and relevant layer/extrusion settings. Let it cool before hand-testing the actual tripod screw. Stop if it binds; record clearance and fit instead of forcing it.

The geometric solid volume is approximately 1.023 cm³. Assuming density 1.05 g/cm³ gives about 1.07 g for a completely solid part, excluding purge and adhesion structures. Use the slicer for the real consumption.

### Roof coupon

The 24 × 18 × 12 mm coupon is an exact slice of the working arm. Its opening faces down, with two feet on the plate. Do not rotate it onto its side: that would no longer test the intended layer sequence. Test without supports beneath the arch. Use a small brim only if needed for bed adhesion.

Inspect the underside at the apex, continuous walls, fallen strands, cracks and separation between layers. Its solid volume is approximately 3.905 cm³ (about 4.10 g at the same assumed density, excluding other extrusion).

A coupon has a different layer time and footprint from the full rig. Passing it is useful evidence but does not prove full-rig printability, large-part shrinkage or stiffness. Neither coupon independently tests the whole upper bracket.

## Full-rig layer inspection

Before sending a job, inspect:

1. Bed contact and brim around both arms and the tower base.
2. Gradual closure of both underside pointed channels.
3. Printed socket entry, thread profile and blind roof; avoid supports trapped inside.
4. Rear tower channel, upper pointed closure, bracket and fully backed marker pad.
5. Marker mounting faces: no unwanted holes, scars or support interfaces.
6. Missing or unexpectedly thin walls, isolated islands, collisions with excluded plate areas, and unusually long bridging paths.

The roof and bracket design reduces unsupported spans; it does not make every surface of the model 60°, nor certify the model as support-free. Add local support only where the actual sliced toolpaths require it and removal is practical.

## Cooling, finishing and assembly

Allow the part to cool before release from the plate. Remove brim carefully without rounding measurement references. Avoid sanding or chemically smoothing the mounting faces: uneven removal changes the centre-height relationships. Remove debris from the socket without damaging its printed thread.

Inspect arm straightness, support perpendicularity and tower stability. Fit the tripod by hand and confirm that tightening does not visibly distort the central boss. Mount identical markers, centre them on each flat face, and use equal adhesive thickness. Do not hide a crack or a loose marker with calibration software settings.

Record the print, measurements and any changes using the [physical test template](../validation/physical-test-record.csv). Keep the actual slicer project locally with the results so that a successful print can be repeated; review it for personal paths and printer identifiers before sharing it.

## Marker subsets on the single v7 rig

- **Vicon:** use O, X150 and Z150 for manual origin setting; Y150 is optional as a check. Leave M100 empty.
- **Motive Custom Calibration Square:** use O, M100 and Y150 only. Leave X150 and Z150 empty or fully mask their reflections. Select these three markers explicitly. See the [Motive workflow](optitrack-workflow.md).

M100 is a fifth mounting position, not a requirement to attach five markers simultaneously. Inspect the roof beneath its pedestal in the slicer; the existing small roof coupon does not test this new loaded section.
