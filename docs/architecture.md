# Architecture

Dalil uses a `src` layout and keeps each concern in an independent,
separately testable layer.

```
src/dalil/
├── __init__.py     # public API: __version__, trace
├── py.typed        # PEP 561 marker
├── _types.py       # shared type aliases / protocols
├── exceptions.py   # DalilError hierarchy
├── decorator.py    # @trace (bare and called forms)
├── tracer/         # line-by-line execution tracing
├── flowchart/      # AST -> graph model -> DOT/Mermaid/SVG
├── complexity/     # static complexity estimation
├── report/         # HTML reports (Jinja2) + templates/
└── latex/          # AST -> LaTeX algorithm
```

## Principles

- Each subpackage exposes a small public API through `__init__.py`.
- No cross-imports between layers, except through public APIs.
- `mypy --strict` must pass; type hints everywhere.
- Google-style docstrings on every public symbol.
- Raise `DalilError` subclasses, never bare `Exception`.
- The decorated function's behavior and return value never change.
- The tracer always restores `sys.settrace`, even on exceptions.

## Data flow

1. `decorator.trace` captures the function metadata.
2. `flowchart` builds the static graph from the AST.
3. `tracer` records execution events while the function runs.
4. `complexity` estimates time / space from the AST.
5. `report` and `latex` render the collected results.
