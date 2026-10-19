"""Nominal tests for the tracer public API: models and stubs."""

from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given
from hypothesis import strategies as st

from dalil.tracer import ExecutionHistory, LineEvent, Tracer
from tests import samples


def test_line_event_creation_and_equality() -> None:
    first = LineEvent(lineno=4, event="line", locals_snapshot={"n": 3}, timestamp=1.5)
    second = LineEvent(lineno=4, event="line", locals_snapshot={"n": 3}, timestamp=1.5)
    assert first == second
    assert first.lineno == 4
    assert first.event == "line"
    assert first.locals_snapshot == {"n": 3}
    assert first.timestamp == 1.5


def test_line_event_inequality() -> None:
    first = LineEvent(lineno=1, event="call")
    second = LineEvent(lineno=2, event="call")
    assert first != second


def test_line_event_defaults() -> None:
    event = LineEvent(lineno=1, event="call")
    assert event.locals_snapshot == {}
    assert isinstance(event.timestamp, float)


def test_line_event_is_frozen() -> None:
    event = LineEvent(lineno=1, event="call")
    with pytest.raises(FrozenInstanceError):
        event.lineno = 2  # type: ignore[misc]


def test_execution_history_creation_and_equality() -> None:
    first = ExecutionHistory(function="f")
    second = ExecutionHistory(function="f")
    assert first == second
    assert first.events == []
    assert second.events == []


def test_execution_history_defaults() -> None:
    history = ExecutionHistory()
    assert history.function == "<unknown>"
    assert history.events == []


def test_execution_history_instances_do_not_share_events() -> None:
    first = ExecutionHistory(function="f")
    second = ExecutionHistory(function="f")
    first.add(LineEvent(lineno=1, event="call"))
    assert first.events != []
    assert second.events == []


def test_execution_history_add_appends_in_order() -> None:
    history = ExecutionHistory(function="f")
    events = [LineEvent(lineno=i, event="line") for i in range(3)]
    for event in events:
        history.add(event)
    assert history.events == events


def test_tracer_initializes_an_empty_history() -> None:
    tracer = Tracer(samples.fibonacci)
    assert tracer.func is samples.fibonacci
    assert isinstance(tracer.history, ExecutionHistory)
    assert tracer.history.function == "fibonacci"
    assert tracer.history.events == []


def test_tracer_enter_is_not_implemented() -> None:
    tracer = Tracer(samples.fibonacci)
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        with tracer:
            pass


def test_tracer_exit_is_not_implemented() -> None:
    tracer = Tracer(samples.fibonacci)
    with pytest.raises(NotImplementedError, match="not implemented yet"):
        tracer.__exit__(None, None, None)


@given(st.dictionaries(st.text(max_size=5), st.integers(), max_size=5))
def test_line_event_stores_the_given_snapshot(data: dict[str, object]) -> None:
    event = LineEvent(lineno=1, event="line", locals_snapshot=data)
    assert event.locals_snapshot == data


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_tracer_collects_line_events() -> None:
    with Tracer(samples.fibonacci) as tracer:
        samples.fibonacci(5)
    assert tracer.history.events
    assert any(event.event == "line" for event in tracer.history.events)


@pytest.mark.xfail(strict=True, reason="not implemented yet")
def test_tracer_records_locals() -> None:
    with Tracer(samples.fibonacci) as tracer:
        samples.fibonacci(5)
    snapshots = [event.locals_snapshot for event in tracer.history.events]
    assert any("n" in snapshot for snapshot in snapshots)
