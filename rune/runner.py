import heapq
from collections import deque
from dataclasses import dataclass

from rune.model import Count, Explore, Group, Order, Take
from rune.optimizer import TopK


def _bfs(graph, start):
    distances = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor, _weight in graph.get(node, []):
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    return distances


@dataclass(frozen=True)
class GroupedBucket:
    key: object
    items: list


@dataclass(frozen=True)
class CountedBucket:
    key: object
    count: int


def _extract(item, key):
    if key == "value":
        return item
    return getattr(item, key)


def _tiebreak(item):
    # Deterministic secondary sort key so ties are broken the same way
    # regardless of which algorithm (full sort, heap select, ...) runs the
    # step -- otherwise two backends can disagree on which tied element to
    # keep, which is a real correctness gap, not a rounding difference.
    return getattr(item, "key", item)


def _sort_key(step):
    if step.descending:
        return lambda item: (_extract(item, step.key), -_tiebreak(item))
    return lambda item: (_extract(item, step.key), _tiebreak(item))


def run_step(step, current):
    if isinstance(step, Group):
        buckets = {}
        order = []
        for item in current:
            k = _extract(item, step.key)
            if k not in buckets:
                buckets[k] = []
                order.append(k)
            buckets[k].append(item)
        return [GroupedBucket(key=k, items=buckets[k]) for k in order]
    if isinstance(step, Count):
        return [CountedBucket(key=b.key, count=len(b.items)) for b in current]
    if isinstance(step, Order):
        return sorted(current, key=_sort_key(step), reverse=step.descending)
    if isinstance(step, Take):
        return current[: step.count]
    if isinstance(step, TopK):
        selector = heapq.nlargest if step.descending else heapq.nsmallest
        return selector(step.count, current, key=_sort_key(step))
    if isinstance(step, Explore):
        distances = _bfs(current, step.start)
        if step.target is None:
            return distances
        return distances.get(step.target)
    raise ValueError(f"unsupported step: {step!r}")


def run_program(steps, data):
    current = data
    for step in steps:
        current = run_step(step, current)
    return current
