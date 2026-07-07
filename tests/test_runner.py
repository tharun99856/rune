from rune.model import Count, Group, Order, Take
from rune.optimizer import TopK
from rune.runner import CountedBucket, GroupedBucket, run_program, run_step


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
