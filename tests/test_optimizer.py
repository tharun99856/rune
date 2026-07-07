from rune.model import Count, Group, Order, Take
from rune.optimizer import TopK, optimize


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
