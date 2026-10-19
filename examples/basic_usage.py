"""Target usage of the Dalil decorator.

The function below keeps its exact original behavior; the inspection
methods (``history``, ``flowchart``, ``complexity``, ``to_latex``,
``report``) delegate to the layer modules and currently raise
``NotImplementedError`` because the layers are still stubs.
"""

import dalil


@dalil.trace(report="fibonacci.html", latex=True)
def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main() -> None:
    """Exercise the decorated function and the inspection API.

    Raises:
        NotImplementedError: Never; stub accessors are caught below.
    """
    # 1. The decorated function behaves exactly like the original one.
    print(f"dalil {dalil.__version__}")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"name preserved: {fibonacci.__name__}")

    # 2. The inspection API (stubs for now).
    for label, call in [
        ("history", lambda: fibonacci.history),
        ("flowchart", fibonacci.flowchart),
        ("complexity", fibonacci.complexity),
        ("to_latex", fibonacci.to_latex),
        ("report", lambda: fibonacci.report("fibonacci.html")),
    ]:
        try:
            print(f"{label}: {call()}")
        except NotImplementedError as exc:
            print(f"{label}: not implemented yet ({exc})")


if __name__ == "__main__":
    main()
