import heapq
from dataclasses import dataclass

from rune.model import Count, Group, Order, Take
from rune.optimizer import TopK


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
        return sorted(current, key=lambda item: _extract(item, step.key), reverse=step.descending)
    if isinstance(step, Take):
        return current[: step.count]
    if isinstance(step, TopK):
        selector = heapq.nlargest if step.descending else heapq.nsmallest
        return selector(step.count, current, key=lambda item: _extract(item, step.key))
    raise ValueError(f"unsupported step: {step!r}")


def run_program(steps, data):
    current = data
    for step in steps:
        current = run_step(step, current)
    return current
