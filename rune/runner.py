import functools
import heapq
from collections import deque
from dataclasses import dataclass

from rune.model import Count, Explore, Group, Objective, Order, Take
from rune.optimizer import KadaneScan, TopK


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


def _dijkstra(graph, start):
    distances = {start: 0}
    heap = [(0, start)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances.get(node, float("inf")):
            continue
        for neighbor, weight in graph.get(node, []):
            candidate = dist + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distances


def _is_weighted(graph):
    return any(weight != 1 for edges in graph.values() for _neighbor, weight in edges)


def _has_negative_edge(graph):
    return any(weight < 0 for edges in graph.values() for _neighbor, weight in edges)


def _bellman_ford(graph, start):
    nodes = set(graph)
    for edges in graph.values():
        for neighbor, _weight in edges:
            nodes.add(neighbor)
    distances = {start: 0}
    for _ in range(max(len(nodes) - 1, 0)):
        changed = False
        for node, edges in graph.items():
            base = distances.get(node)
            if base is None:
                continue
            for neighbor, weight in edges:
                candidate = base + weight
                if candidate < distances.get(neighbor, float("inf")):
                    distances[neighbor] = candidate
                    changed = True
        if not changed:
            break
    # After V-1 rounds every shortest path is settled -- unless a further
    # relaxation still improves something, which can only mean a reachable
    # negative cycle, where "shortest" is undefined. Report it; never loop.
    for node, edges in graph.items():
        base = distances.get(node)
        if base is None:
            continue
        for neighbor, weight in edges:
            if base + weight < distances.get(neighbor, float("inf")):
                raise ValueError(
                    f"graph contains a negative cycle reachable from {start!r}; "
                    "shortest distances are undefined"
                )
    return distances


def _better(candidate, best, direction):
    if best is None:
        return True
    return candidate > best if direction == "maximize" else candidate < best


def _objective_contiguous_naive(nums, direction, measure):
    # Baseline: examine every contiguous subarray. O(n^2) with a running sum.
    # This is the honest "check all candidates" implementation the optimizer
    # replaces -- not how you'd write it by hand, but what "maximize sum over
    # contiguous" literally means before any algorithmic insight.
    if measure != "sum":
        raise ValueError(f"unsupported objective measure: {measure!r}")
    if not nums:
        return None
    best = None
    n = len(nums)
    for i in range(n):
        running = 0
        for j in range(i, n):
            running += nums[j]
            if _better(running, best, direction):
                best = running
    return best


@dataclass(frozen=True)
class StrategyExplanation:
    rule: str
    strategy: str
    reason: str


def _select_shortest_path_strategy(graph):
    if _has_negative_edge(graph):
        return _bellman_ford, StrategyExplanation(
            rule="EXPLORE_STRATEGY_SELECTION",
            strategy="Bellman-Ford",
            reason=(
                "Graph has negative-weight edges; Dijkstra's greedy settling "
                "assumes a later edge can never shorten a finished path, which "
                "negative weights break. Bellman-Ford's V-1 relaxation rounds "
                "handle them -- and if a further round still improves a "
                "distance, that's a negative cycle, reported as an error "
                "instead of looping forever."
            ),
        )
    if _is_weighted(graph):
        return _dijkstra, StrategyExplanation(
            rule="EXPLORE_STRATEGY_SELECTION",
            strategy="Dijkstra",
            reason=(
                "Graph has edges with weight other than 1; BFS counts hops, "
                "not weight, and would give the wrong shortest distance, so "
                "Dijkstra's priority-queue relaxation is used instead."
            ),
        )
    return _bfs, StrategyExplanation(
        rule="EXPLORE_STRATEGY_SELECTION",
        strategy="BFS",
        reason=(
            "All edges have uniform weight (unweighted graph); BFS gives "
            "correct shortest paths in O(V+E), with less overhead than "
            "Dijkstra's priority queue."
        ),
    )


def explore_with_explanation(step, graph):
    algorithm, explanation = _select_shortest_path_strategy(graph)
    distances = algorithm(graph, step.start)
    result = distances if step.target is None else distances.get(step.target)
    return result, explanation


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


@functools.total_ordering
class _AscTiebreak:
    # Wraps a tiebreak value so a heap that keeps the "largest" element still
    # resolves ties toward the SMALLEST tiebreak -- the same ascending-tiebreak
    # convention _ordered() uses, but reached by inverting the comparison
    # instead of arithmetic negation, so it works for any orderable key
    # (characters, strings), not just numbers that can be negated.
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return other.value < self.value


def _ordered(current, key, descending):
    # Stable two-stage sort: order by the deterministic tiebreak ascending,
    # then by the primary key in the requested direction. Python's sort is
    # stable, so equal primary keys keep their ascending-tiebreak order in
    # both directions -- and nothing is negated, so non-numeric keys sort as
    # cleanly as numbers do.
    by_tiebreak = sorted(current, key=_tiebreak)
    return sorted(by_tiebreak, key=lambda item: _extract(item, key), reverse=descending)


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
        return _ordered(current, step.key, step.descending)
    if isinstance(step, Take):
        return current[: step.count]
    if isinstance(step, TopK):
        if step.descending:
            return heapq.nlargest(
                step.count,
                current,
                key=lambda item: (_extract(item, step.key), _AscTiebreak(_tiebreak(item))),
            )
        return heapq.nsmallest(
            step.count,
            current,
            key=lambda item: (_extract(item, step.key), _tiebreak(item)),
        )
    if isinstance(step, Explore):
        algorithm, _explanation = _select_shortest_path_strategy(current)
        distances = algorithm(current, step.start)
        if step.target is None:
            return distances
        return distances.get(step.target)
    if isinstance(step, Objective):
        if step.scope != "contiguous":
            raise ValueError(f"unsupported objective scope: {step.scope!r}")
        return _objective_contiguous_naive(current, step.direction, step.measure)
    if isinstance(step, KadaneScan):
        # O(n): the best subarray ending here is either just this element, or
        # this element extending the best subarray ending at the previous one.
        if not current:
            return None
        pick = max if step.direction == "maximize" else min
        best = running = current[0]
        for x in current[1:]:
            running = pick(x, running + x)
            best = pick(best, running)
        return best
    raise ValueError(f"unsupported step: {step!r}")


def run_program(steps, data):
    current = data
    for step in steps:
        current = run_step(step, current)
    return current
