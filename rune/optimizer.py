from dataclasses import dataclass

from rune.model import Objective, Order, Take


@dataclass(frozen=True)
class TopK:
    key: str
    descending: bool
    count: int


@dataclass(frozen=True)
class KadaneScan:
    direction: str  # "maximize" | "minimize"


@dataclass(frozen=True)
class RewriteExplanation:
    rule: str
    before: str
    after: str
    reason: str


def _coalesce_takes(steps):
    # Fold back-to-back TAKEs into a single tightest bound. TAKE a then TAKE b
    # is the first b of the first a rows -- the first min(a, b) either way --
    # so one bound replaces two, and it runs before the ORDER+TAKE fusion so
    # the resulting heap is sized to the tighter bound.
    out = []
    explanations = []
    for step in steps:
        if isinstance(step, Take) and out and isinstance(out[-1], Take):
            prev = out[-1]
            tighter = min(prev.count, step.count)
            out[-1] = Take(count=tighter)
            explanations.append(
                RewriteExplanation(
                    rule="COALESCE_TAKES",
                    before=f"TAKE {prev.count} + TAKE {step.count}",
                    after=f"TAKE {tighter}",
                    reason=(
                        "Consecutive TAKEs each only bound the length; keeping just the "
                        "smaller bound yields the same rows without the redundant pass."
                    ),
                )
            )
        else:
            out.append(step)
    return out, explanations


def optimize(steps):
    steps, explanations = _coalesce_takes(steps)
    new_steps = []
    i = 0
    while i < len(steps):
        step = steps[i]
        if isinstance(step, Order) and i + 1 < len(steps) and isinstance(steps[i + 1], Take):
            take = steps[i + 1]
            new_steps.append(TopK(key=step.key, descending=step.descending, count=take.count))
            direction = "DESC" if step.descending else "ASC"
            explanations.append(
                RewriteExplanation(
                    rule="ORDER_TAKE_TO_TOP_K",
                    before=f"ORDER BY {step.key} {direction} + TAKE {take.count}",
                    after=f"TOP_K({step.key}, {take.count})",
                    reason=(
                        "ORDER immediately followed by TAKE recognized as top-k "
                        "selection; a heap of size k avoids fully sorting the input."
                    ),
                )
            )
            i += 2
        elif isinstance(step, Objective) and step.measure == "sum" and step.scope == "contiguous":
            new_steps.append(KadaneScan(direction=step.direction))
            explanations.append(
                RewriteExplanation(
                    rule="OBJECTIVE_CONTIGUOUS_TO_KADANE",
                    before=f"{step.direction.upper()} SUM OVER CONTIGUOUS {step.source}",
                    after=f"KADANE({step.direction}) -- O(n) single pass",
                    reason=(
                        "Objective is the best sum over contiguous subarrays; optimal "
                        "substructure means the best subarray ending at each position "
                        "extends the best one ending just before it, so a single pass "
                        "(Kadane's) replaces checking all O(n^2) subarrays."
                    ),
                )
            )
            i += 1
        else:
            new_steps.append(step)
            i += 1
    return new_steps, explanations
