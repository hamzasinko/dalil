# Dalil

**Dalil** (Arabic for *guide*) is a Python library that makes code execution
understandable. A single decorator adds a visual flowchart, a line-by-line
execution trace, an algorithmic-complexity estimate, an HTML report, and a
LaTeX algorithm export to any function.

```python
import dalil


@dalil.trace
def binary_search(items, target): ...
```

## Features

- **Flowchart** — AST to DOT / Mermaid / SVG.
- **Tracing** — variables, branches and returns per executed line.
- **Complexity** — static time / space estimation.
- **Report** — standalone HTML report (Jinja2).
- **LaTeX** — `algorithm2e` / `algorithmicx` output.

## Project status

Early skeleton: the public API is defined, implementations raise
`NotImplementedError`.

## Next steps

- [Architecture](architecture.md)
- [Usage](usage.md)
