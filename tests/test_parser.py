from lang.model import Count, Group, Order, Take
from lang.parser import parse_program


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
