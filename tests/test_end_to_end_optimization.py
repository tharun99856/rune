from rune.optimizer import optimize
from rune.parser import parse_program
from rune.runner import run_program


def test_optimized_and_naive_execution_produce_identical_results():
    program = (
        "GROUP nums BY value\n"
        "COUNT EACH group\n"
        "ORDER BY count DESC\n"
        "TAKE 3"
    )
    data = [5, 5, 5, 5, 2, 2, 2, 7, 7, 9, 9, 9, 9, 9]

    graph = parse_program(program)

    naive_result = run_program(graph.steps, data)

    optimized_steps, explanations = optimize(graph.steps)
    optimized_result = run_program(optimized_steps, data)

    naive_pairs = [(b.key, b.count) for b in naive_result]
    optimized_pairs = [(b.key, b.count) for b in optimized_result]
    assert naive_pairs == optimized_pairs == [(9, 5), (5, 4), (2, 3)]

    assert len(explanations) == 1
    assert explanations[0].rule == "ORDER_TAKE_TO_TOP_K"
