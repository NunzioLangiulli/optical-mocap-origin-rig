# OptiTrack / Motive: single v7 rig

One full-rig STL serves both systems. V7 adds M100 at CAD (100,0,24) mm while retaining O/X150/Y150/Z150. **The geometry satisfies the documented custom-square requirement; physical printing and Motive operation remain untested.**

## Use three markers

| Mount | Face centre (mm) | Role |
| --- | --- | --- |
| O | (0,0,24) | Right-angle vertex |
| M100 | (100,0,24) | Short arm, 100 mm |
| Y150 | (0,150,24) | Long arm, 150 mm |

Leave X150 and Z150 empty or completely mask their reflections. Use identical markers, equal adhesive thickness and accurate centring. Nominal M100-to-Y150 distance is 180.28 mm. These dimensions are not a calibrated length standard.

## Set origin after camera calibration

Motive specifies a right-angle three-marker custom square with unequal arms. Select Custom, enter the measured vertical offset, select the three markers and set the ground plane using the controls in the installed version. [Official calibration instructions](https://docs.optitrack.com/motive/calibration).

Level the arms for a gravity-aligned plane. Measure the offset from marker centres to the intended plane; do not assume 24 mm, which describes only the mounting-face height above the printed base. On a tripod the intended plane may be above the floor. Verify origin, axis directions, plane height and repeatability, including after occlusion.

The design labels are not Motive axis labels. Motive uses Y up. Check the displayed directions rather than assuming the [coordinate conversion example](compatibility.md) is automatically applied by Custom square. This rig does not replace camera wand calibration.

## Optional rigid-body method

This is unnecessary for the three-marker procedure. Populating all five positions breaks the original four-marker cyclic symmetry, a geometric deduction rather than a tested tracking result. OptiTrack recommends asymmetric marker layouts. Correct pivot pose and reacquisition checks remain necessary, particularly when M100 is hidden. [Rigid-body guidance](https://docs.optitrack.com/motive/rigid-body-tracking).

## Vicon configuration

Use O/X150/Z150 for the Nexus manual origin procedure, optionally Y150 as a check. Leave M100 unused. See [Nexus workflow](nexus-workflow.md). No second printed model is required. Record results in the [test template](../validation/physical-test-record.csv).
