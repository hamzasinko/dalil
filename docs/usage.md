# Usage

## Installation

```bash
pip install dalil
# optional extras
pip install "dalil[viz]" "dalil[cli]"
```

## Decorating a function

Bare form:

```python
import dalil


@dalil.trace
def sum_until(limit: int) -> int:
    total = 0
    i = 0
    while i < limit:
        total += i
        i += 1
    return total
```

Called form:

```python
@dalil.trace(report="out/report.html", latex=True)
def parse(text: str) -> dict: ...
```

The wrapper keeps the original behavior, return value and metadata, and
adds the inspection API:

```python
sum_until(100)  # behaves exactly like the plain function
sum_until.history  # ExecutionHistory  -> NotImplementedError (stub)
sum_until.flowchart()  # FlowGraph         -> NotImplementedError (stub)
sum_until.complexity()  # ComplexityResult  -> NotImplementedError (stub)
sum_until.to_latex()  # str               -> NotImplementedError (stub)
sum_until.report("o.html")  # str             -> NotImplementedError (stub)
```

## Building the pieces by hand

```python
from dalil import complexity, flowchart, latex, report, tracer

graph = flowchart.build_flowgraph(func)
dot = flowchart.to_dot(graph)
mermaid = flowchart.to_mermaid(graph)

result = complexity.estimate(func)  # ComplexityResult

history = tracer.ExecutionHistory(function="func")
event = tracer.LineEvent(lineno=4, event="line", locals_snapshot={"x": 1})
history.add(event)

with tracer.Tracer(func):  # NotImplementedError (stub)
    ...

report.generate_report(history, graph, result, "out/report.html")
algorithm = latex.to_latex(func)
```

## Error handling

```python
from dalil.exceptions import DalilError

try:
    ...
except DalilError as exc:
    print(exc.message, exc.cause)
```

## Status

Every layer is currently a skeleton: the models (`LineEvent`,
`ExecutionHistory`, `Node`, `Edge`, `FlowGraph`, `ComplexityResult`) are
real, the functions raise `NotImplementedError`.
