# Contributing

Useful contributions include reproducible print reports, measured dimensional results, improved tripod compatibility and geometry fixes. Please distinguish simulations, slicing, printed results and actual Nexus operation.

For a print report, provide the design/model hash, printer, nozzle, material, slicer version/settings, orientation, support/brim choices and photographs. Include measurement method and uncertainty when reporting dimensions. Remove personal data, printer credentials and unrelated laboratory or participant information.

For a code/design change:

1. Explain the problem and the intended geometric or user-visible result.
2. Keep marker coordinates and axes explicit; update all dependent features when changing them.
3. Run the build, geometry tests and repository checks documented in `docs/development.md`.
4. Inspect the exported STL and any updated renders. Include relevant validation rather than claiming that a passing mesh check proves printability.
5. Update documentation and release evidence if changing the reference model. Avoid changing a released file silently under an existing hash.

Use English for public documentation and issues. Code contributions are under MIT; design, model and documentation contributions are under CC BY 4.0, consistent with `LICENSE`. State the origin and license of any third-party material; do not include proprietary manufacturer assets.
