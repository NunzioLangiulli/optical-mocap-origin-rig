# Publishing this prepared repository

No GitHub repository or release has been created by this preparation package. The destination account, repository URL and visibility are not assumed.

## Suggested metadata

**Name:** `optical-mocap-origin-rig`

**Description:** 3D-printable origin reference rig for optical motion capture. Vicon Nexus and OptiTrack Motive workflows, five marker positions, CAD source and STL. Physical validation pending.

**Topics:** `optical-motion-capture`, `motion-capture`, `mocap`, `origin-rig`, `coordinate-system`, `vicon`, `vicon-nexus`, `optitrack`, `motive`, `3d-printing`, `stl`, `cad`, `research-tools`

**Suggested first tag:** `v0.2.0` (contains mechanical design `v7`).

The name describes the technology and function without tying the project to one manufacturer. Keep the expanded phrase **optical motion capture**, the origin/ground-plane purpose, and the supported workflow names in the README and repository description. These terms help readers find the project; search-engine ranking and universal compatibility are not guaranteed.

## Create and push

Create an **empty** repository in your intended GitHub account/organization. Choose visibility intentionally. Do not add a generated README or single-license template: this folder already has both licenses and a scope statement.

From this folder, after reviewing the content:

```sh
git init -b main
git add .
git commit -m "Prepare origin rig v7 with English documentation and geometry checks"
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
```

`<YOUR_REPOSITORY_URL>` is the actual HTTPS or SSH URL returned by GitHub, not a literal command argument. Use your own configured Git author identity and normal authentication. No token should be placed in project files or command history. If this folder has already been initialized, `git init` can be omitted.

After the first push, inspect the rendered README and wait for the **Digital geometry checks** workflow. The preparation-time checks ran locally; GitHub status is not assumed. Check the license rendering as GitHub may not display a single standard badge for the mixed-license layout.

## Release assets

Run `python scripts/package_release.py` to create a clean archive under `dist/`. The source ZIP contains printable STLs, documentation, source, tests and licensing; it excludes virtual environments, caches and build files.

Attach the archive and, optionally, the three individual STLs plus `validation/SHA256SUMS.txt` to a release. Use the text in [release notes](release-notes.md). Mark the initial release as a **pre-release** to make the untested physical status visible.

Update `NOTICE.md` with the actual public repository link for convenient attribution. Add photos and any successful print record only after testing. Do not upload local manufacturer PDFs, historical working folders, `.cad_dependencies`, G-code containing printer-specific assumptions, or machine credentials.
