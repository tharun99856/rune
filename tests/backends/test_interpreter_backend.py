from rune.backends.interpreter_backend import InterpreterBackend
from rune.model import Count, Group, Order, Take


def test_interpreter_backend_supports_any_steps():
    backend = InterpreterBackend()

    assert backend.supports([Group(source="nums", key="value")]) is True
    assert backend.supports([]) is True


def test_interpreter_backend_runs_top_k_frequent():
    backend = InterpreterBackend()
    steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        Order(key="count", descending=True),
        Take(count=2),
    ]

    result = backend.run(steps, [1, 1, 1, 2, 2, 3, 4, 4, 4, 4])

    assert [b.key for b in result] == [4, 1]
