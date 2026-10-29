# Validation evidence and limits

## Current evidence

| Stage | Status at preparation of this repository |
| --- | --- |
| CAD dimensions and design intent | Defined; critical features digitally checked |
| Exported STL integrity | Checked for all three supplied files |
| Portable generator versus existing v7 STL | Compared within explicit geometric tolerances |
| English preview images | Rendered from the supplied rig STL and inspected |
| Local automated tests | Results in the validation report |
| GitHub Actions | Workflow provided; remote run not yet observed |
| Bambu Studio slicing | Not performed/validated for this release |
| ABS coupon prints | No physical result recorded |
| Full rig print and dimensional survey | Not performed/validated |
| Mechanical, tripod and optical visibility tests | Not performed/validated |
| Motive use/repeatability | Not performed/validated |
| Nexus use/repeatability | Not performed/validated |

The source of truth for mesh metrics is [`geometry_report.json`](../validation/geometry_report.json). [`SHA256SUMS.txt`](../validation/SHA256SUMS.txt) identifies the supplied assets. Hashes check file identity, not print quality.

## Digital checks

Each mesh is cleaned conservatively, exported and reopened. Checks include watertightness, consistent winding, positive volume, one connected component and expected bounds. A nominal 0.02 mm geometric simplification is used to remove numerical degeneracies. Its tolerance is not a physical manufacturing tolerance.

Regression tests additionally probe material and empty space at marker faces, cylindrical supports, channels, socket and upper-pad backing. Nominal marker vectors are checked for 150 mm lengths and mutual orthogonality. The added M100 position, its backing, open channel, and 100/150 mm right-angle triangle are also checked. A symmetric-difference comparison helps detect shape changes that could be missed by checking volume alone.

The full-rig STL was regenerated for v7; the two original coupon STLs are retained. Consolidating the original multi-file generation chain can change triangulation under Boolean operations and simplification. Rebuild comparisons therefore use geometric tolerances rather than requiring byte-identical STL hashes: maximum exported-mesh volume difference 10 mm³ and source-solid versus reference-mesh symmetric-difference volume 30 mm³. These comparisons use different stages of the mesh pipeline, so their values need not be ordered. These are software regression thresholds, not acceptable experimental errors. Actual results are reported separately.

## What the checks cannot establish

- Whether the slicer generates suitable paths for the point closures, thread and bracket.
- Whether a given ABS batch/profile produces strong layer bonds or acceptable shrinkage.
- Whether the printed arms remain straight, the tower rigid or the tripod thread durable.
- Whether actual markers fit, remain centred and are visible in your camera arrangement.
- Whether origin placement meets the spatial/angular tolerance needed by an experiment.

No finite-element analysis, thread-gauge measurement, load rating, calibration certificate or manufacturer approval is claimed.

## Physical validation plan

### 1. Define acceptance criteria first

Choose dimensional, angular and repeatability tolerances appropriate to the intended experiment. This repository does not invent a universal acceptable error. Record the tolerances, measuring instruments and method before interpreting measurements. A normal caliper may not be sufficient to establish optical-centre positions accurately.

### 2. Record the print conditions

Record printer/nozzle, plate, filament brand/type/colour/batch, drying, layer height, widths, wall count, infill, brim/supports, temperature/cooling settings, slicer version and model hash. Record changes separately so a failure can be traced to a particular configuration.

### 3. Coupon checks

For the thread, use the actual screw after cooling and record whether it engages smoothly, binds, rocks or bottoms out. For the roof, inspect both inclined faces and their meeting point. Reject detached strands or layer separation that could affect later printing. A passing coupon is not a full-size validation.

### 4. Full-rig inspection

After cooling, inspect the underside, cylindrical feet, tower and upper bracket. Measure appropriate reference distances and arm angles independently of Nexus. Check flatness and whether tightening onto the tripod deforms the central area. Measure or estimate measurement uncertainty; do not present more precision than the method supports.

### 5. Marker and optical checks

Verify identical marker construction and mounting height, centring, adhesion and visibility. Document any low-angle occlusion caused by the Ø18 mm supports. The printed geometry is only one component of the final marker-centre geometry.

### 6. Operational repeatability

Use the normal camera-calibration workflow, set the origin with this rig, and repeat placement/selection according to a documented protocol. Distinguish repeatability of the selected frame from absolute accuracy, and distinguish moving the rig from leaving it untouched. Use independent references when assessing absolute position or orientation.

Use the provided [CSV record](../validation/physical-test-record.csv); empty result fields mean **not tested**, not passed. When publishing results, include photographs and relevant settings without disclosing credentials, serial numbers or unrelated participant data.

## Cross-system validation status

Official software documentation has been reviewed for Nexus and Motive; neither system has been tested with the printed rig. No other vendor workflow has been assessed. Verify marker identity, origin position, axis direction, scale, repeatability, and behavior after occlusion/reacquisition for each system and version. The OptiTrack limitations are documented in the [compatibility guide](compatibility.md); a passing mesh test does not establish reliable optical marker identification.
