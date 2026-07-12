import shutil
import subprocess
import sys

import pytest

from rune.backends.cpp_backend import CppBackend, emit_cpp
from rune.optimizer import KadaneScan


def _zig_available():
    try:
        subprocess.run(
            [sys.executable, "-m", "ziglang", "version"],
            capture_output=True, check=True, timeout=30,
        )
        return True
    except Exception:
        return False


def test_emit_cpp_generates_maximize_and_minimize_variants():
    src_max = emit_cpp([KadaneScan(direction="maximize")])
    src_min = emit_cpp([KadaneScan(direction="minimize")])

    assert "int main" in src_max
    assert "fscanf" in src_max  # reads the data file
    # the two directions must differ (opposite comparisons)
    assert src_max != src_min


def test_cpp_backend_supports_only_the_kadane_plan():
    backend = CppBackend()

    assert backend.supports([KadaneScan(direction="maximize")]) is True
    assert backend.supports([]) is False


requires_zig = pytest.mark.skipif(not _zig_available(), reason="zig (ziglang) not installed")


@requires_zig
def test_cpp_backend_compiles_runs_and_matches_interpreter():
    from rune.runner import run_step

    data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    step = KadaneScan(direction="maximize")

    cpp_result = CppBackend().run([step], data)
    interp_result = run_step(step, data)

    assert cpp_result == interp_result == 6


@requires_zig
def test_cpp_backend_handles_all_negative_minimize_and_empty():
    assert CppBackend().run([KadaneScan(direction="maximize")], [-3, -1, -2]) == -1
    assert CppBackend().run([KadaneScan(direction="minimize")], [3, -2, 5, -1, -4, 2]) == -5
    assert CppBackend().run([KadaneScan(direction="maximize")], []) is None


def _topk_plan(k=3):
    from rune.optimizer import optimize
    from rune.parser import parse_program

    graph = parse_program(f"GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE {k}")
    optimized, _ = optimize(graph.steps)
    return optimized  # [Group, Count, TopK]


def test_emit_cpp_generates_topk_plan():
    src = emit_cpp(_topk_plan(3))
    assert "int main" in src
    assert "sort" in src  # top-k selection needs ordering by count


def test_cpp_backend_supports_the_topk_plan():
    assert CppBackend().supports(_topk_plan(3)) is True


@requires_zig
def test_cpp_topk_matches_interpreter_including_tie_break():
    from rune.runner import run_program

    # data with a deliberate count tie (2 and 7 both appear 3 times) so the
    # tie-break (count desc, key asc) actually matters and C++ must match it.
    data = [5, 5, 5, 5, 9, 9, 9, 2, 2, 2, 7, 7, 7, 1]
    plan = _topk_plan(3)

    interp = [(b.key, b.count) for b in run_program(plan, data)]
    cpp = [(b.key, b.count) for b in CppBackend().run(plan, data)]

    assert cpp == interp
