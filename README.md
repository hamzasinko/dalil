# Dalil · دليل

**Understand your Python code, one decoration at a time.**

[![CI](https://github.com/dalil-python/dalil/actions/workflows/ci.yml/badge.svg)](https://github.com/dalil-python/dalil/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A590%25-brightgreen)](https://github.com/dalil-python/dalil/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/dalil.svg)](https://pypi.org/project/dalil/)
[![Python](https://img.shields.io/pypi/pyversions/dalil.svg)](https://pypi.org/project/dalil/)
[![License: MIT](https://img.shields.io/pypi/l/dalil.svg)](LICENSE)

*Dalil* (دليل — Arabic for *guide*) makes code execution understandable. A single
decorator turns any Python function into a visual flowchart, a line-by-line
execution trace, a complexity estimate, an HTML report, and a LaTeX algorithm.

## Why Dalil?

Reading someone else's code — or your own from six months ago — is hard.
Debuggers show *state*, not *story*. Dalil tells the story of a function: how it
branches, what it computes at each line, how costly it is, and how to present it
in a course, a paper, or a pull request.

- **Educators**: show students exactly what their loop does, step by step.
- **Learners**: paste a function, read the flowchart, understand the complexity.
- **Authors**: export a clean `algorithm2e` listing straight from real code.

## Features

| # | Feature | Status |
|---|---------|--------|
| 1 | `@trace` decorator that never changes behavior | 🚧 skeleton |
| 2 | Flowchart from the AST (DOT / Mermaid) | 📋 planned |
| 3 | SVG rendering via the optional `graphviz` extra | 📋 planned |
| 4 | Line-by-line execution trace (variables, branches, returns) | 📋 planned |
| 5 | Time / space complexity estimation | 📋 planned |
| 6 | Standalone HTML report (Jinja2) | 📋 planned |
| 7 | LaTeX export (`algorithm2e` / `algorithmicx`) and rich CLI output | 📋 planned |

## Installation

```bash
pip install dalil
# optional extras
pip install "dalil[viz]"   # graphviz SVG rendering
pip install "dalil[cli]"   # rich console output
```

Requires Python >= 3.9.

## Quick start

```python
import dalil


@dalil.trace
def binary_search(items: list[int], target: int) -> int:
    """Return the index of target in sorted items, or -1."""
    low, high = 0, len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


binary_search([1, 3, 5, 7], 5)  # behaves exactly like the plain function
binary_search.flowchart()  # -> FlowGraph       (planned)
binary_search.complexity()  # -> ComplexityResult (planned)
binary_search.to_latex()  # -> LaTeX source     (planned)
binary_search.report("out.html")  # -> HTML report      (planned)
binary_search.history  # -> ExecutionHistory (planned)
```

> **Status**: the public API is defined; the layers are still stubs that raise
> `NotImplementedError`. See the [roadmap](#roadmap).

## Architecture

```
src/dalil/
├── decorator.py    # @trace: @trace and @trace(...) forms
├── tracer/         # line-by-line execution events (LineEvent, Tracer)
├── flowchart/      # AST -> graph model -> DOT / Mermaid / SVG
├── complexity/     # static time / space estimation
├── report/         # HTML reports (Jinja2 templates)
├── latex/          # AST -> LaTeX algorithm
├── exceptions.py   # DalilError hierarchy
└── _types.py       # shared type aliases
```

Each layer is independent and separately testable; see
[docs/architecture.md](docs/architecture.md).

## Roadmap

- [x] Project skeleton, packaging, CI, docs scaffolding
- [x] Public decorator API (`@trace`, wrapped inspection methods)
- [ ] AST to flowchart graph model + DOT / Mermaid output
- [ ] SVG rendering (optional `graphviz` extra)
- [ ] Execution tracer with safe `sys.settrace` handling
- [ ] Complexity estimation (loops, nesting, recursion)
- [ ] HTML report with Jinja2 templates
- [ ] LaTeX export (`algorithm2e` / `algorithmicx`)
- [ ] Rich CLI output (optional `cli` extra)
- [ ] 1.0 release on PyPI

## Contributing

Contributions welcome! Read [CONTRIBUTING.md](CONTRIBUTING.md) for the setup,
code conventions, and PR process. In short:

1. Fork and create a `feature/<short-name>` branch **from `dev`**.
2. Add tests (nominal + edge), keep coverage >= 90%.
3. Run `pytest`, `ruff check .`, `ruff format --check .`, `mypy --strict src tests`.
4. Open a PR against `dev` using the template (Conventional Commits).

Branch flow: `feature/*` → `dev` → `main` → `prod` (releases).

Please note that this project follows a
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

MIT © [Dalil Contributors](LICENSE).

## Acknowledgments

- Python's `ast`, `inspect` and `sys.settrace` machinery that makes this possible.
- The [algorithm2e](https://ctan.org/pkg/algorithm2e) and Mermaid projects for
  two great ways to describe algorithms.
- Everyone who files an issue, reviews a PR, or teaches with code.
