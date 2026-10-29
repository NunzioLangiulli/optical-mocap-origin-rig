# Setting the origin in Nexus

## Purpose and prerequisite

This rig is used **after camera calibration** to establish a coordinate origin and axis orientation. It does not estimate camera intrinsic/extrinsic parameters and does not replace an Active Wand. The 150 mm dimensions are design targets, not certified scale references.

Vicon documents a *Three Markers* option that asks for an origin marker, a primary X-axis marker and a secondary Z-axis marker. Follow the prompts in your installed Nexus version if labels or layout differ. The source workflow is linked in [references](references.md); this exact printed rig has not yet been tested in Nexus.

## Identify the markers

- **O:** lower marker above the central tripod boss.
- **X:** end of the horizontal arm in the positive CAD X direction.
- **Y:** end of the other horizontal arm, in the positive CAD Y direction.
- **Z:** highest marker, directly above O.

The two horizontal arms are visually similar. The STL has no embossed axis letters. Before use, identify X/Y from the documented geometry or the reference views and label the body unobtrusively. Do not select them by apparent left/right position on a camera image, which changes with viewpoint. Avoid reflective labels that create extra detections.

## Procedure

1. Calibrate the camera system using its normal supported calibration device and procedure. Review the calibration feedback before proceeding.
2. Fix the printed rig to the tripod and place it where the origin should be. Stabilise the tripod, then orient the arms toward your intended positive directions.
3. If global Z should match gravity, level the rig independently. Nexus follows the selected marker geometry; a tilted tripod does not become level through origin setting.
4. Attach/check O, X150, Y150 and Z150; leave M100 empty. In a live 3D perspective view, confirm that O, X and Z are reconstructed and distinguishable, and that their positions are stable.
5. In **System Preparation → Set Volume Origin**, use **Three Markers → Set** as provided by your version.
6. Select **O**, then **X**, then **Z**, following the on-screen prompts. Do not select Y as the documented secondary Z marker.
7. Inspect the resulting global coordinate axes. X should point from O towards X; Z should point towards the top marker. Verify the positive Y direction using the fourth marker and the software view.
8. Confirm that the origin coincides with the reconstructed centre of O and that the result remains stable when the rig is untouched. Record the software version, print revision and checks performed.

The fourth marker adds a check point; it does not automatically improve the three-point origin fit or make the rig a calibrated reference. Do not create a new labeling skeleton merely to perform the documented manual origin-selection workflow.

## Height and orientation interpretation

The mounting surface for O is 24 mm above the bottom of the print. Its marker centre is higher by the unknown marker-specific offset `h`. Thus, a nominal `Z=0` at O in Nexus is not the floor, tripod plate, or bottom of the rig. If an application needs an origin on another surface, establish and document the offset through an appropriate, separately verified workflow.

Likewise, setting an origin from three imperfectly placed markers does not repair a warped rig. Software may still display an orthogonal world frame even when the four physical marker positions deviate from the intended orthogonal arrangement.

## Troubleshooting

| Observation | Check |
| --- | --- |
| Marker is missing or intermittent | Camera visibility, reflections, marker shape and obstruction by the supports/tower |
| Positive Y is opposite to the intended direction | X/Y identification, selected marker order, orientation of the physical rig |
| Origin is higher than the tripod plate | Expected: it is at O's reconstructed marker centre |
| Axes are tilted relative to the room | Physical leveling and marker attachment; do not infer gravity from the CAD |
| Origin changes between attempts | Marker stability, tripod movement, incorrect selection, reconstruction consistency |
| Distances differ from 150 mm | Measure the cooled rig and marker centring independently; also review the already-established camera calibration |
| Good software feedback but visible print deformation | Do not treat software feedback as dimensional certification of the rig |

Record observations rather than compensating blindly by scaling the STL. Marker placement, shrinkage and system calibration are different possible causes and require different checks.
