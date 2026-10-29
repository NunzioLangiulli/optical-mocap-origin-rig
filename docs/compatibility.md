# Compatibility with optical motion-capture systems

This is a passive-marker coordinate reference, not a manufacturer-specific electronic device. Its physical role can extend beyond Vicon to other optical motion-capture systems that reconstruct suitable retroreflective markers. **A usable physical reference does not imply compatibility with a software package's automatic origin tool.** No physical system has yet been tested with this design.

| System / workflow | Assessment for the released v7 |
| --- | --- |
| Vicon Nexus, manual Three Markers | Documented workflow matches the intended O → X → Z selection; hardware validation pending. See [Nexus guide](nexus-workflow.md). |
| OptiTrack Motive, Custom Calibration Square | Use O/M100/Y150: 100/150 mm arms at 90 degrees. Documented geometry satisfied; physical use untested. See [OptiTrack assessment](optitrack-workflow.md). |
| OptiTrack Motive, rigid-body origin | Software provides this route, but the five-position v7 layout has not been tested as an automatically identified asset. Requires resolving identity and checking pivot pose. |
| Other passive optical systems | Potential physical reference if the system can reconstruct and identify the markers; native origin procedure must be checked for the exact software/version. No vendor-specific support is claimed. |
| Exported, correctly labelled 3D coordinates | Can define a local reference frame using the construction below, independently of native origin controls. This does not modify the camera calibration. |
| Markerless or inertial-only systems | No direct compatibility established: the rig alone does not provide their required observations or calibration inputs. |

## Requirements across systems

Confirm marker material, shape, size, visibility and reconstruction quality with the actual cameras. A nominal 12 mm adhesive marker is not sufficient evidence of optical suitability. All marker centres used in the chosen workflow must be identified correctly; printed axis labels are for a human and are not optically encoded marker IDs. Measure the printed rig after cooling and use the actual marker-centre geometry when assessing accuracy. The 150 mm CAD distances are nominal, not a traceable scale calibration.

The frame origin is marker O's reconstructed centre. A floor or tripod origin requires an explicitly measured offset. “Up” follows the mounted rig unless it is independently levelled; the model does not measure gravity.

## System-independent local frame from labelled points

Given reconstructed positions `o`, `x`, `y`, `z` in a common coordinate system and unit:

1. Set `ex = normalize(x - o)`.
2. Remove the X component from the Z direction: `v = (z - o) - dot(z - o, ex) * ex`; set `ez = normalize(v)`.
3. Set `ey = cross(ez, ex)` and form the matrix `R = [ex ey ez]` with these vectors as columns.
4. Express any point `p` in the rig frame as `p_local = transpose(R) * (p - o)`.

Reject missing, mislabelled or nearly collinear input before normalization. Check that Y is on the positive `ey` side and compare all measured distances, angles and residuals against experiment-specific acceptance criteria. The orthogonalization above produces a mathematical frame even for a distorted print; it does **not** prove that the print is orthogonal. It privileges O/X/Z, with Y as a check. No implementation or live software integration is supplied by this documentation.

## Axis conventions

This project's labels describe a right-handed Z-up frame. For a right-handed Y-up convention, one possible mapping is `x_new = x_rig`, `y_new = z_rig`, `z_new = -y_rig`. This is a proper rotation (determinant +1). Merely swapping Y and Z would reflect the frame. Verify axis signs and exported data conventions for the destination system; this mapping is a project choice, not an automatic setting applied by the STL.

## Reporting compatibility

Record system model, software/version, marker type, origin method, axis convention, measured offsets, and repeatability in the [test record](../validation/physical-test-record.csv). Test identity after occlusion and reacquisition as well as during an uninterrupted view. A successful result on one setup does not establish universal compatibility.
