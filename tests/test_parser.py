import pytest

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


def test_unrecognized_step_names_the_line_and_the_word():
    with pytest.raises(ValueError) as exc:
        parse_program("GROUP nums BY value\nFILTER x")

    message = str(exc.value)
    assert "line 2" in message
    assert "FILTER" in message
    assert "GROUP" in message  # tells you what a step CAN start with


def test_incomplete_step_names_the_line_and_expected_form():
    with pytest.raises(ValueError) as exc:
        parse_program("TAKE")

    message = str(exc.value)
    assert "line 1" in message
    assert "TAKE <count>" in message


def test_non_numeric_take_count_gets_the_expected_form():
    with pytest.raises(ValueError) as exc:
        parse_program("TAKE many")

    message = str(exc.value)
    assert "line 1" in message
    assert "TAKE <count>" in message


def test_blank_lines_do_not_shift_reported_line_numbers():
    with pytest.raises(ValueError) as exc:
        parse_program("\nGROUP nums BY value\n\nBOGUS x")

    assert "line 4" in str(exc.value)


def test_trailing_tokens_are_rejected_not_silently_dropped():
    # 'TAKE 5 please' used to parse as TAKE 5 -- silent tolerance of junk
    # undermines verification (a hallucinated proposal with trailing tokens
    # must be REJECTED, not quietly accepted).
    with pytest.raises(ValueError, match="TAKE <count>"):
        parse_program("TAKE 5 please")
    with pytest.raises(ValueError, match="GROUP <source> BY <key>"):
        parse_program("GROUP nums BY value extra junk")


def test_computed_group_key_is_rejected_not_mangled():
    # Hypothesis 2 spelling from the relation candidate: used to "parse" as
    # key='(target' with '- value)' silently dropped. Must reject instead.
    with pytest.raises(ValueError, match="GROUP <source> BY <key>"):
        parse_program("GROUP nums BY (target - value)")


def test_wrong_inner_keywords_are_rejected():
    with pytest.raises(ValueError):  # BANANA is not ASC|DESC
        parse_program("ORDER BY count BANANA")
    with pytest.raises(ValueError):  # X is not TO
        parse_program("EXPLORE graph FROM a X b")
    with pytest.raises(ValueError):  # ALL is not EACH
        parse_program("COUNT ALL group")
    with pytest.raises(ValueError):  # only SUM is in the grammar today
        parse_program("MAXIMIZE PRODUCT OVER CONTIGUOUS nums")
