# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Project skeleton with `src/` layout, `py.typed` and shared type aliases
  (`dalil._types`).
- Public `dalil.trace` decorator supporting `@trace` and `@trace(...)`,
  preserving behavior, return value and metadata via `functools.update_wrapper`.
- `TracedFunction` wrapper exposing `.history`, `.flowchart()`,
  `.complexity()`, `.to_latex()` and `.report(path)` (layers are stubs).
- Tracer models: `LineEvent`, `ExecutionHistory`, `Tracer` context manager.
- Flowchart models: `Node`, `Edge`, `FlowGraph`, `build_flowgraph`.
- Complexity model: `ComplexityResult` and `estimate`.
- Report layer: `generate_report` and a minimal Jinja2 template
  (`report/templates/report.html.j2`).
- LaTeX layer: `to_latex` stub.
- Exception hierarchy rooted at `DalilError` (`TraceError`,
  `FlowchartError`, `ComplexityError`, `ReportError`, `LatexError`).
- Test suite (pytest + Hypothesis): 96 nominal/edge tests, 19 strict xfails
  for not-yet-implemented behavior, coverage >= 90%.
- Packaging with hatchling (dynamic version, extras `viz`, `cli`, `dev`,
  `docs`), ruff / mypy / pytest / coverage configuration.
- CI workflow (lint, 5x3 test matrix, build), release workflow with PyPI
  Trusted Publishing, Dependabot configuration.
- Open-source files: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE
  (MIT), issue and PR templates, CODEOWNERS.

## [0.1.0] - Unreleased

Initial development version. The public API is defined; the flowchart,
tracer, complexity, report and LaTeX layers raise `NotImplementedError`.

[Unreleased]: https://github.com/dalil-python/dalil/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/dalil-python/dalil/releases/tag/v0.1.0
