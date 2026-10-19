# Contributing to Dalil

Thanks for your interest in contributing! This document describes the
development setup, coding conventions, and the pull-request process.

## Development setup

```bash
git clone https://github.com/dalil-python/dalil.git
cd dalil
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pre-commit install               # optional: hooks run ruff + mypy
```

Python >= 3.9 is required.

## Running the checks

```bash
python -m pytest                                  # tests + coverage (fail-under 90)
python -m pytest tests/unit                       # nominal tests only
python -m pytest tests/edge                       # edge cases only
python -m pytest -m "not xfail" -rx               # show unexpected xfails
python -m ruff check .                            # lint
python -m ruff format .                           # format
python -m mypy --strict src tests                 # type check
python -m build && twine check dist/*             # packaging sanity
```

All checks must pass before a PR can be merged. Coverage must stay >= 90%.

## Code conventions

- **Type hints everywhere**; `mypy --strict` must pass.
- **Docstrings**: Google style, in English, on every public module, class and
  function.
- **Formatting**: `ruff format` + `ruff check` (line length 88).
- **Naming**: `snake_case` functions/modules, `PascalCase` classes,
  `UPPER_CASE` constants.
- **Errors**: raise `DalilError` subclasses, never bare `Exception`.
- **No global mutable state**; the tracer must restore `sys.settrace` even when
  an exception escapes.
- The decorated function's **behavior and return value must never change**.
- Layers are independent: **no cross-imports** except through public APIs.

## Tests

- Mirror the package layout: `tests/unit/<module>/test_*.py` (nominal) and
  `tests/edge/<module>/test_*.py` (edge cases).
- Every feature needs nominal tests **and** edge cases: empty functions,
  recursion, generators, exceptions, nested functions, lambdas, async, stacked
  decorators, concurrent calls.
- Use [Hypothesis](https://hypothesis.readthedocs.io/) for property-based tests
  where relevant.
- Tests of not-yet-implemented behavior are marked
  `@pytest.mark.xfail(strict=True, reason="not implemented yet")` instead of
  being omitted.

## Git workflow and branches

| Branch | Role |
|--------|------|
| `main` | stable, reviewed code |
| `dev` | integration branch — **start feature branches here** |
| `prod` | production releases (pushing here triggers a release) |
| `feature/<short-name>` | new features, based on `dev` |
| `fix/<short-name>` | bug fixes, based on `dev` |
| `docs/<short-name>` | documentation, based on `dev` |

Flow: `feature/*` → (PR) → `dev` → (PR) → `main` → `prod`.

```mermaid
gitGraph
    commit id: "chore: initial project skeleton" tag: "v0.1.0"
    branch dev
    checkout dev
    commit id: "feat: ..."
    branch feature/tracer-core
    checkout feature/tracer-core
    commit id: "feat(tracer): ..."
    commit id: "test(tracer): ..."
    checkout dev
    merge feature/tracer-core id: "PR #12 (1 review, CI green)"
    checkout main
    merge dev id: "PR: release candidate"
    checkout prod
    merge main tag: "v0.2.0"
```

Every arrow above is a pull request protected by branch protection:

- `main`, `dev` and `prod` require a PR, **1 approving review**, a linear
  history (squash/rebase only), no force-push, and the required status checks
  `lint`, `test`, `build`.
- `prod` additionally restricts merges to maintainers.
- `feature/*`, `fix/*` and `docs/*` are free to push; they may only land in
  `dev` through a PR.

Never push directly to `main`, `dev` or `prod`.

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add flowchart graph model
fix: restore sys.settrace on tracer exception
docs: explain the report template context
test: cover stacked decorators
chore: pin hypothesis in dev extras
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`,
`build`. Scope is optional: `feat(complexity): estimate nested loops`.

## Pull-request process

1. Open the PR **against `dev`** (not `main`) using the PR template.
2. Link the related issue (`Closes #123`).
3. Fill in the "How to test" section with reproducible steps.
4. Ensure the checklist is complete: tests (nominal + edge), coverage >= 90%,
   `ruff` + `mypy` clean, docs and `CHANGELOG.md` updated.
5. At least one review is required; CI must be green.
6. Squash-merge is preferred; keep the Conventional Commit title.

## Reporting bugs and proposing features

Use the [issue templates](https://github.com/dalil-python/dalil/issues/new/choose).
For security issues, see [SECURITY.md](SECURITY.md) — do **not** open a public
issue.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
