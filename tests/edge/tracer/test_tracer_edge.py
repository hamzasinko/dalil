"""Edge-case tests for the tracer layer: model independence and stubs."""

import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given
from hypothesis import strategies as st

from dalil.tracer import ExecutionHistory, LineEvent, Tracer
from tests import samples


def test_histories_are_independent_between_tracers() -> None:
    first = Tracer(samples.fibonacci)
    second = Tracer(samples.fibonacci)
    assert first.history is not second.history


def test_snapshot_payload_is_mutable_but_field_is_frozen() -> None:
    event = LineEvent(lineno=1, event="line", locals_snapshot={"n": 1})
    event.locals_snapshot["n"] = 2  # payload mutable
    assert event.locals_snapshot == {"n": 2}
    with pytest.raises(FrozenInstanceError):
        event.locals_snapshot = {}  # type: ignore[misc]


def test_history_events_field_is_rebindable() -> None:
    history = ExecutionHistory(function="f")
    history.events = []
    assert history.events == []


def test_concurrent_history_appends_stay_isolated() -> None:
    def work(index: int) -> int:
        history = ExecutionHistory(function=f"f{index}")
        for line in range(10):
            history.add(LineEvent(lineno=line, event="line"))
        return len(history.events)

    with ThreadPoolExecutor(max_workers=8) as pool:
        counts = list(pool.map(work, range(32)))
    assert counts == [10] * 32


def test_stub_errors_leave_sys_settrace_untouched() -> None:
    previous = sys.gettrace()
    for func in (samples.fibonacci, samples.bubble_sort):
        tracer = Tracer(func)
        with pytest.raises(NotImplementedError, match="not implemented yet"):
            with tracer:
                pass
    assert sys.gettrace() is previous


@given(st.lists(st.integers(min_value=-50, max_value=50), max_size=20))
def test_event_counts_match_appended_batches(lines: list[int]) -> None:
    history = ExecutionHistory(function="f")
    for lineno in lines:
        history.add(LineEvent(lineno=lineno, event="line"))
    assert [event.lineno for event in history.events] == lines
