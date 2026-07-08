import pytest

numba = pytest.importorskip("numba")

from rune.backends.numba_backend import NumbaBackend
from rune.model import Count, Group, Order, Take
from rune.optimizer import TopK


def test_numba_backend_supports_group_count_topk_shape():
    backend = NumbaBackend(domain_size=10)
    steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        TopK(key="count", descending=True, count=2),
    ]

    assert backend.supports(steps) is True


def test_numba_backend_rejects_unrecognized_shapes():
    backend = NumbaBackend(domain_size=10)

    assert backend.supports([Order(key="count", descending=True), Take(count=2)]) is False
    assert backend.supports([Group(source="nums", key="value")]) is False


def test_numba_backend_produces_same_result_as_interpreter():
    from rune.backends.interpreter_backend import InterpreterBackend

    data = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    interpreter_steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        Order(key="count", descending=True),
        Take(count=2),
    ]
    numba_steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        TopK(key="count", descending=True, count=2),
    ]

    interpreter_result = InterpreterBackend().run(interpreter_steps, data)
    numba_result = NumbaBackend(domain_size=5).run(numba_steps, data)

    interpreter_pairs = sorted((b.key, b.count) for b in interpreter_result)
    numba_pairs = sorted((b.key, b.count) for b in numba_result)
    assert interpreter_pairs == numba_pairs


def test_numba_backend_breaks_ties_identically_to_interpreter():
    # Deliberately tied data: values 1, 2, 3 all occur exactly twice, so a
    # naive comparison could pass by coincidence. Exact order must match --
    # this is the case that surfaced a real cross-backend disagreement.
    from rune.backends.interpreter_backend import InterpreterBackend

    data = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4]
    interpreter_steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        Order(key="count", descending=True),
        Take(count=3),
    ]
    numba_steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        TopK(key="count", descending=True, count=3),
    ]

    interpreter_result = InterpreterBackend().run(interpreter_steps, data)
    numba_result = NumbaBackend(domain_size=5).run(numba_steps, data)

    interpreter_pairs = [(b.key, b.count) for b in interpreter_result]
    numba_pairs = [(b.key, b.count) for b in numba_result]
    assert interpreter_pairs == numba_pairs == [(4, 4), (1, 2), (2, 2)]
