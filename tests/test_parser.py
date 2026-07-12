from rune.model import Count, Explore, Group, Objective, Order, Take
from rune.parser import parse_program


def test_parses_take_line():
    graph = parse_program("TAKE 10")

    assert graph.steps == [Take(count=10)]


def test_parses_order_by_desc_line():
    graph = parse_program("ORDER BY count DESC")

    assert graph.steps == [Order(key="count", descending=True)]


def test_parses_order_by_defaults_to_ascending():
    graph = parse_program("ORDER BY count")

    assert graph.steps == [Order(key="count", descending=False)]


def test_parses_group_by_line():
    graph = parse_program("GROUP nums BY value")

    assert graph.steps == [Group(source="nums", key="value")]


def test_parses_count_each_line():
    graph = parse_program("COUNT EACH group")

    assert graph.steps == [Count(noun="group")]


def test_parses_full_top_k_frequent_pipeline():
    program = "\n".join(
        [
            "GROUP nums BY value",
            "COUNT EACH group",
            "ORDER BY count DESC",
            "TAKE 10",
        ]
    )

    graph = parse_program(program)

    assert graph.steps == [
        Group(source="nums", key="value"),
        Count(noun="group"),
        Order(key="count", descending=True),
        Take(count=10),
    ]


def test_parses_explore_from_line():
    graph = parse_program("EXPLORE graph FROM a")

    assert graph.steps == [Explore(source="graph", start="a", target=None)]


def test_parses_explore_from_to_line():
    graph = parse_program("EXPLORE graph FROM a TO b")

    assert graph.steps == [Explore(source="graph", start="a", target="b")]


def test_parses_maximize_sum_over_contiguous():
    graph = parse_program("MAXIMIZE SUM OVER CONTIGUOUS nums")

    assert graph.steps == [
        Objective(direction="maximize", measure="sum", scope="contiguous", source="nums")
    ]


def test_parses_minimize_variant():
    graph = parse_program("MINIMIZE SUM OVER CONTIGUOUS nums")

    assert graph.steps == [
        Objective(direction="minimize", measure="sum", scope="contiguous", source="nums")
    ]
