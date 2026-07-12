import random

from rune.optimizer import optimize
from rune.parser import parse_program
from rune.runner import run_program


def test_parse_optimize_run_maximize_sum_contiguous():
    graph = parse_program("MAXIMIZE SUM OVER CONTIGUOUS nums")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

    naive = run_program(graph.steps, nums)

    optimized_steps, explanations = optimize(graph.steps)
    optimized = run_program(optimized_steps, nums)

    assert naive == optimized == 6
    assert len(explanations) == 1
    assert explanations[0].rule == "OBJECTIVE_CONTIGUOUS_TO_KADANE"


def test_naive_and_kadane_agree_on_200_random_arrays():
    # The real correctness guarantee: not hand-picked cases, but the optimizer
    # and the baseline agreeing across a wide random sample, including
    # all-negative and single-element arrays.
    graph = parse_program("MAXIMIZE SUM OVER CONTIGUOUS nums")
    optimized_steps, _ = optimize(graph.steps)
    rng = random.Random(7)

    for _ in range(200):
        n = rng.randint(1, 40)
        nums = [rng.randint(-20, 20) for _ in range(n)]
        naive = run_program(graph.steps, nums)
        optimized = run_program(optimized_steps, nums)
        assert naive == optimized, nums
