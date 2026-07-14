from rune.model import Count, Explore, Group, Objective, Order, Take
from rune.optimizer import TopK
from rune.runner import (
    CountedBucket,
    GroupedBucket,
    explore_with_explanation,
    run_program,
    run_step,
)


def test_group_by_value_buckets_identical_items():
    data = [1, 2, 2, 3, 3, 3]
    step = Group(source="nums", key="value")

    result = run_step(step, data)

    assert result == [
        GroupedBucket(key=1, items=[1]),
        GroupedBucket(key=2, items=[2, 2]),
        GroupedBucket(key=3, items=[3, 3, 3]),
    ]


def test_count_each_group_counts_bucket_sizes():
    buckets = [
        GroupedBucket(key=1, items=[1]),
        GroupedBucket(key=2, items=[2, 2]),
        GroupedBucket(key=3, items=[3, 3, 3]),
    ]
    step = Count(noun="group")

    result = run_step(step, buckets)

    assert result == [
        CountedBucket(key=1, count=1),
        CountedBucket(key=2, count=2),
        CountedBucket(key=3, count=3),
    ]


def test_order_by_count_descending_sorts_buckets():
    buckets = [
        CountedBucket(key=1, count=1),
        CountedBucket(key=2, count=3),
        CountedBucket(key=3, count=2),
    ]
    step = Order(key="count", descending=True)

    result = run_step(step, buckets)

    assert [b.key for b in result] == [2, 3, 1]


def test_take_returns_first_n():
    buckets = [
        CountedBucket(key=2, count=3),
        CountedBucket(key=3, count=2),
        CountedBucket(key=1, count=1),
    ]
    step = Take(count=2)

    result = run_step(step, buckets)

    assert [b.key for b in result] == [2, 3]


def test_run_program_executes_top_k_frequent_end_to_end():
    data = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    steps = [
        Group(source="nums", key="value"),
        Count(noun="group"),
        Order(key="count", descending=True),
        Take(count=2),
    ]

    result = run_program(steps, data)

    assert [b.key for b in result] == [4, 1]
    assert [b.count for b in result] == [4, 3]


def test_order_breaks_ties_by_ascending_bucket_key():
    buckets = [
        CountedBucket(key=30, count=5),
        CountedBucket(key=10, count=5),
        CountedBucket(key=20, count=5),
    ]
    step = Order(key="count", descending=True)

    result = run_step(step, buckets)

    assert [b.key for b in result] == [10, 20, 30]


def test_top_k_breaks_ties_the_same_way_as_order_does():
    buckets = [
        CountedBucket(key=30, count=5),
        CountedBucket(key=10, count=5),
        CountedBucket(key=20, count=5),
        CountedBucket(key=40, count=9),
    ]
    step = TopK(key="count", descending=True, count=2)

    result = run_step(step, buckets)

    assert [b.key for b in result] == [40, 10]


def test_order_descending_over_string_keys_does_not_crash():
    # Regression: descending ORDER over buckets whose key is non-numeric (a
    # character, from GROUP text BY value / COUNT EACH char) must not crash.
    # The primary sorts by count descending; ties break by ascending key --
    # the same convention as numeric keys, just without assuming the key can
    # be arithmetically negated.
    buckets = [
        CountedBucket(key="t", count=1),
        CountedBucket(key="e", count=2),
        CountedBucket(key="r", count=1),
    ]
    step = Order(key="count", descending=True)

    result = run_step(step, buckets)

    assert [b.key for b in result] == ["e", "r", "t"]


def test_top_k_over_string_keys_breaks_ties_like_order():
    # The optimized TOP_K path must handle string keys identically to ORDER,
    # so switching on the optimizer can't change results for non-numeric keys.
    buckets = [
        CountedBucket(key="t", count=1),
        CountedBucket(key="e", count=2),
        CountedBucket(key="r", count=1),
    ]
    step = TopK(key="count", descending=True, count=2)

    result = run_step(step, buckets)

    assert [b.key for b in result] == ["e", "r"]


def test_top_k_step_selects_highest_by_key_without_full_sort():
    buckets = [
        CountedBucket(key=1, count=3),
        CountedBucket(key=2, count=1),
        CountedBucket(key=3, count=4),
        CountedBucket(key=4, count=2),
    ]
    step = TopK(key="count", descending=True, count=2)

    result = run_step(step, buckets)

    assert [b.key for b in result] == [3, 1]
    assert [b.count for b in result] == [4, 3]


def test_explore_without_target_returns_bfs_distances_from_start():
    # unweighted adjacency: node -> list of (neighbor, weight)
    graph = {
        "a": [("b", 1), ("c", 1)],
        "b": [("d", 1)],
        "c": [("d", 1)],
        "d": [],
        "e": [],  # unreachable from a
    }
    step = Explore(source="graph", start="a", target=None)

    result = run_step(step, graph)

    assert result == {"a": 0, "b": 1, "c": 1, "d": 2}


def test_explore_with_target_returns_shortest_hop_count():
    graph = {
        "a": [("b", 1), ("c", 1)],
        "b": [("d", 1)],
        "c": [("d", 1)],
        "d": [],
    }

    result = run_step(Explore(source="graph", start="a", target="d"), graph)

    assert result == 2


def test_explore_with_unreachable_target_returns_none():
    graph = {"a": [("b", 1)], "b": [], "z": []}

    result = run_step(Explore(source="graph", start="a", target="z"), graph)

    assert result is None


# Chosen so that fewest-hops (a->b, 1 hop, weight 5) disagrees with
# lowest-weight (a->c->b, 2 hops, weight 2) -- BFS-by-hop-count would give
# the wrong answer here. Only Dijkstra gets this right.
_WEIGHTED_GRAPH = {
    "a": [("b", 5), ("c", 1)],
    "b": [("d", 1)],
    "c": [("b", 1), ("d", 10)],
    "d": [],
}


def test_explore_picks_bfs_and_explains_why_for_unweighted_graphs():
    graph = {"a": [("b", 1)], "b": [("c", 1)], "c": []}

    result, explanation = explore_with_explanation(
        Explore(source="graph", start="a", target=None), graph
    )

    assert result == {"a": 0, "b": 1, "c": 2}
    assert explanation.strategy == "BFS"
    assert "unweighted" in explanation.reason.lower() or "weight" in explanation.reason.lower()


def test_explore_picks_dijkstra_and_explains_why_for_weighted_graphs():
    result, explanation = explore_with_explanation(
        Explore(source="graph", start="a", target=None), _WEIGHTED_GRAPH
    )

    assert result == {"a": 0, "c": 1, "b": 2, "d": 3}
    assert explanation.strategy == "Dijkstra"


def test_run_step_uses_dijkstra_automatically_for_weighted_graphs():
    # The default execution path (no explanation needed) must still be
    # correct -- BFS on a weighted graph would silently give the wrong
    # hop-count-based answer instead of the true shortest weighted distance.
    result = run_step(Explore(source="graph", start="a", target="b"), _WEIGHTED_GRAPH)

    assert result == 2


def test_maximize_sum_contiguous_classic_kadane_case():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    step = Objective(direction="maximize", measure="sum", scope="contiguous", source="nums")

    result = run_step(step, nums)

    assert result == 6  # subarray [4, -1, 2, 1]


def test_maximize_sum_contiguous_all_negative_returns_largest_single():
    nums = [-3, -1, -2]
    step = Objective(direction="maximize", measure="sum", scope="contiguous", source="nums")

    assert run_step(step, nums) == -1


def test_minimize_sum_contiguous():
    nums = [3, -2, 5, -1, -4, 2]
    step = Objective(direction="minimize", measure="sum", scope="contiguous", source="nums")

    assert run_step(step, nums) == -5  # subarray [-1, -4]


def test_objective_on_empty_returns_none():
    step = Objective(direction="maximize", measure="sum", scope="contiguous", source="nums")

    assert run_step(step, []) is None


def test_kadane_scan_matches_naive_on_classic_case():
    from rune.optimizer import KadaneScan

    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    naive = run_step(
        Objective(direction="maximize", measure="sum", scope="contiguous", source="nums"), nums
    )
    kadane = run_step(KadaneScan(direction="maximize"), nums)

    assert kadane == naive == 6


def test_kadane_scan_minimize_and_all_negative_and_empty():
    from rune.optimizer import KadaneScan

    assert run_step(KadaneScan(direction="minimize"), [3, -2, 5, -1, -4, 2]) == -5
    assert run_step(KadaneScan(direction="maximize"), [-3, -1, -2]) == -1
    assert run_step(KadaneScan(direction="maximize"), []) is None
