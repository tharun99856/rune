from rune.model import Count, Group, Objective, Order, Take
from rune.optimizer import KadaneScan, TopK, optimize


def test_order_take_adjacent_pair_rewrites_to_top_k():
    steps = [Order(key="count", descending=True), Take(count=10)]

    new_steps, explanations = optimize(steps)

    assert new_steps == [TopK(key="count", descending=True, count=10)]
    assert len(explanations) == 1


def test_explanation_names_the_rule_and_gives_a_reason():
    steps = [Order(key="count", descending=True), Take(count=10)]

    _, explanations = optimize(steps)

    exp = explanations[0]
    assert exp.rule == "ORDER_TAKE_TO_TOP_K"
    assert "heap" in exp.reason.lower()
    assert "ORDER" in exp.before and "TAKE" in exp.before


def test_group_and_count_pass_through_unchanged_in_full_pipeline():
    steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        Order(key="count", descending=True),
        Take(count=10),
    ]

    new_steps, explanations = optimize(steps)

    assert new_steps == [
        Group(source="nums", key="value"),
        Count(noun="group"),
        TopK(key="count", descending=True, count=10),
    ]
    assert len(explanations) == 1


def test_order_without_a_following_take_is_not_rewritten():
    steps = [Order(key="count", descending=True)]

    new_steps, explanations = optimize(steps)

    assert new_steps == [Order(key="count", descending=True)]
    assert explanations == []


def test_maximize_sum_contiguous_rewrites_to_kadane_with_explanation():
    steps = [Objective(direction="maximize", measure="sum", scope="contiguous", source="nums")]

    new_steps, explanations = optimize(steps)

    assert new_steps == [KadaneScan(direction="maximize")]
    assert len(explanations) == 1
    exp = explanations[0]
    assert exp.rule == "OBJECTIVE_CONTIGUOUS_TO_KADANE"
    assert "O(n)" in exp.after or "single pass" in exp.reason.lower()
    assert "subarray" in exp.reason.lower()


def test_objective_with_non_contiguous_scope_is_not_rewritten():
    # Only the contiguous scope has the Kadane rewrite. A different scope must
    # pass through untouched, not get silently mis-optimized.
    steps = [Objective(direction="maximize", measure="sum", scope="pairs", source="nums")]

    new_steps, explanations = optimize(steps)

    assert new_steps == steps
    assert explanations == []
