# Dalil: Project Context for AI Assistants

## Vision
Dalil ("guide" in Arabic) is an open-source Python library that makes code
execution understandable. A single decorator `@dalil.trace` on a function:
1. Converts the function into a visual flowchart (from its AST).
2. Traces what happens at each line during execution (variables, branches, return).
3. Estimates the algorithmic complexity (time / space) of the function.
4. Generates a full HTML report with the execution history.
5. Exports the algorithm to LaTeX (algorithm2e / algorithmicx style).

The public API exists; the layer implementations are still stubs that raise
`NotImplementedError` (tracked by strict xfail tests).

## Tech stack
- Python >= 3.9 (CI matrix: 3.9, 3.10, 3.11, 3.12, 3.13 x Linux/macOS/Windows)
- src layout, package name `dalil`, hatchling build backend, dynamic version
  read from `src/dalil/__init__.py`
- Runtime deps (keep minimal): `jinja2` (HTML reports)
- Optional extras: `viz` (`graphviz`), `cli` (`rich`), `docs` (`mkdocs-material`)
- Dev deps: pytest, pytest-cov, hypothesis, ruff, mypy, pre-commit, build, twine
- Core techniques: `ast`, `inspect`, `sys.settrace`, `functools.update_wrapper`

## Repository layout
- `src/dalil/decorator.py` : public `trace` decorator (`@trace` / `@trace(...)`)
  and the `TracedFunction` wrapper (incl. `__get__` for method binding)
- `src/dalil/tracer/`      : line-by-line execution tracing, event models
- `src/dalil/flowchart/`   : AST -> graph model -> DOT / Mermaid / SVG
- `src/dalil/complexity/`  : static complexity estimation (loops, recursion)
- `src/dalil/report/`      : HTML report generation; template in
  `report/templates/report.html.j2`
- `src/dalil/latex/`       : AST -> LaTeX algorithm conversion
- `src/dalil/exceptions.py`: exception hierarchy (base: `DalilError`)
- `src/dalil/_types.py`    : shared type aliases / protocols
- `tests/unit/<module>/`   : nominal tests
- `tests/edge/<module>/`   : edge cases (empty function, recursion, generators,
  exceptions, nested functions, lambdas, async, stacked decorators, threads)
- `tests/conftest.py`      : shared fixtures; `tests/samples.py`: sample functions
- `docs/`                  : MkDocs pages (index, architecture, usage)
- `examples/`              : runnable examples
Each subpackage exposes a small public API via `__init__.py`; no cross-imports
except through public APIs. Layers are independent and separately testable.

## Commands
Required to pass before any merge:
- `python -m pip install -e ".[dev]"`
- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy src` (CI also checks tests: `python -m mypy --strict src tests`)
- `python -m pytest` (coverage >= 90%, branch coverage, `--strict-markers`)
- `python -m build` then `python -m twine check dist/*`

## Coding conventions
- Type hints everywhere; `mypy --strict` must pass.
- Docstrings: Google style, in English, on every public module/class/function.
- Formatting and linting: `ruff format` + `ruff check` (line length 88).
- Naming: snake_case functions/modules, PascalCase classes, UPPER_CASE constants.
- No global mutable state; tracer must restore `sys.settrace` even on exceptions.
- The decorated function's behavior and return value must never change.
- Raise `DalilError` subclasses, never bare `Exception`.

## Testing rules
- pytest, tests mirror the package: `tests/unit/<module>/test_*.py` (nominal)
  and `tests/edge/<module>/test_*.py` (edge cases).
- Every feature needs: nominal tests + edge cases (empty function, recursion,
  generators, exceptions, nested functions, lambdas, async, decorators stacking).
- Coverage must stay >= 90% (CI fails below; current coverage is 100%).
- Unimplemented behavior is covered by `@pytest.mark.xfail(strict=True,
  reason="not implemented yet")` tests, never omitted.
- Use `hypothesis` for property-based tests where relevant.

## CI / packaging
- `.github/workflows/ci.yml`: jobs `lint`, `tests` (matrix, uploads coverage),
  `test` (gate on the matrix), `build` (sdist/wheel + `twine check`).
- `.github/workflows/release.yml`: on push to `prod` or `v*.*.*` tag; runs tests,
  builds, publishes via PyPI Trusted Publishing (requires a PyPI trusted
  publisher for `hamzasinko/dalil`, workflow `release.yml`, env `pypi`), then
  creates a GitHub Release.
- Dependabot covers pip and GitHub Actions weekly (`.github/dependabot.yml`).

## Git workflow
- Branches: `main` (stable), `dev` (default, integration), `prod` (releases),
  `feature/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.
- Feature branches start from `dev` and are merged via PR into `dev`.
- `dev` -> `main` via PR when stable; `main` -> `prod` to release.
- Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- Never push directly to `main`, `dev` or `prod`.
- Protection on `main`/`dev`/`prod`: PR required, 1 approving review, required
  checks `lint`, `test`, `build`, linear history, no force-push, no deletion.
  `prod` restrictions are the same: merge access is limited to repository
  writers (personal repository limitation; move to an organization to add
  explicit user/team restrictions).
- Repository: https://github.com/hamzasinko/dalil

## Definition of done
Code + type hints + docstrings + tests (nominal and edge) + passing CI +
updated docs/CHANGELOG + PR using the template.
